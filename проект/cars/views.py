from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, Q, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime
from rest_framework import permissions, viewsets

from .forms import (
    BookingCreateForm,
    CarManageForm,
    RegisterForm,
    UserCreateForm,
    UserManageForm,
    UserPasswordChangeForm,
)
from .models import Booking, BookingMessage, BookingStatus, BookingStatusHistory, Car
from .serializers import BookingSerializer, CarSerializer

BOOKING_PRIORITY_ORDER = Case(
    When(status=BookingStatus.CREATED, then=0),
    default=1,
    output_field=IntegerField(),
)


def _add_status_history(booking, from_status, to_status, changed_by=None, comment=""):
    """Сохраняет одну запись о смене статуса бронирования."""
    BookingStatusHistory.objects.create(
        booking=booking,
        from_status=from_status,
        to_status=to_status,
        changed_by=(
            changed_by if getattr(changed_by, "is_authenticated", False) else None
        ),
        comment=comment or "",
    )


def _user_can_access_booking(booking, user):
    """Возвращает True, если пользователь владелец брони или сотрудник."""
    return booking.user_id == user.id or user.is_staff


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    """Публичный API только для чтения списка активных автомобилей."""

    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Car.objects.filter(is_active=True)
        car_class = self.request.query_params.get("class")
        if car_class:
            queryset = queryset.filter(car_class=car_class)
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    """API для авторизованного пользователя и его бронирований."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects.filter(user=self.request.user)
            .select_related("car")
            .order_by(BOOKING_PRIORITY_ORDER, "-created_at")
        )


def landing_page(request):
    """Отрисовывает лендинг со списком активных авто и фильтрами по классу."""
    selected_class = request.GET.get("class", "all")
    cars_qs = Car.objects.filter(is_active=True)

    context = {
        "cars": cars_qs,
        "selected_class": selected_class,
        "classes": [
            ("all", "Все"),
            ("business", "Бизнес"),
            ("suv", "SUV"),
            ("comfort", "Комфорт"),
            ("economy", "Эконом"),
        ],
    }
    return render(request, "cars/index.html", context)


def car_detail(request, car_id):
    """Показывает карточку авто и позволяет создать бронирование."""
    car = get_object_or_404(Car, pk=car_id, is_active=True)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/login/?next=/cars/{car.id}/")

        form = BookingCreateForm(request.POST, user=request.user, car=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование создано.")
            return redirect("my_bookings")
    else:
        form = BookingCreateForm(
            user=request.user if request.user.is_authenticated else None, car=car
        )

    return render(request, "cars/car_detail.html", {"car": car, "form": form})


def register_view(request):
    """Регистрирует нового пользователя и автоматически авторизует его."""
    if request.user.is_authenticated:
        return redirect("landing")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("landing")
    else:
        form = RegisterForm()
    return render(request, "cars/register.html", {"form": form})


@login_required
def my_bookings(request):
    """Показывает брони пользователя с приоритетом новых заявок сверху."""
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("car")
        .order_by(BOOKING_PRIORITY_ORDER, "-created_at")
    )
    return render(request, "cars/my_bookings.html", {"bookings": bookings})


@login_required
def booking_chat(request, booking_id):
    """Показывает чат по брони и обрабатывает отправку новых сообщений."""
    booking = get_object_or_404(
        Booking.objects.select_related("user", "car"), pk=booking_id
    )

    is_manager = request.user.is_staff
    if not _user_can_access_booking(booking, request.user):
        messages.error(request, "Нет доступа к чату этой брони.")
        return redirect("landing")

    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if text:
            BookingMessage.objects.create(
                booking=booking, author=request.user, text=text
            )
            return redirect("booking_chat", booking_id=booking.id)
        messages.error(request, "Сообщение не может быть пустым.")

    chat_messages_qs = booking.messages.select_related("author")
    chat_paginator = Paginator(chat_messages_qs, 20)
    chat_page_number = request.GET.get("page", 1)
    chat_page_obj = chat_paginator.get_page(chat_page_number)

    return render(
        request,
        "cars/booking_chat.html",
        {
            "booking": booking,
            "chat_messages": chat_page_obj.object_list,
            "chat_page_obj": chat_page_obj,
            "is_manager": is_manager,
        },
    )


@login_required
def booking_chat_messages(request, booking_id):
    """Возвращает JSON с пагинацией сообщений для автообновления чата."""
    booking = get_object_or_404(Booking.objects.select_related("user"), pk=booking_id)

    if not _user_can_access_booking(booking, request.user):
        return JsonResponse({"error": "forbidden"}, status=403)

    page_number = request.GET.get("page", 1)
    messages_qs = booking.messages.select_related("author")
    paginator = Paginator(messages_qs, 20)
    page_obj = paginator.get_page(page_number)

    items = []
    for msg in page_obj.object_list:
        items.append(
            {
                "author": msg.author.username,
                "created_at": msg.created_at.strftime("%d.%m.%Y %H:%M"),
                "text": msg.text,
            }
        )

    return JsonResponse(
        {
            "messages": items,
            "page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "num_pages": paginator.num_pages,
        }
    )


@login_required
def cancel_booking(request, booking_id):
    """Позволяет клиенту отменить только новые или подтвержденные брони."""
    if request.method != "POST":
        return redirect("my_bookings")

    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status in [BookingStatus.CREATED, BookingStatus.CONFIRMED]:
        previous_status = booking.status
        booking.status = BookingStatus.CANCELED
        booking.save(update_fields=["status"])
        _add_status_history(
            booking=booking,
            from_status=previous_status,
            to_status=BookingStatus.CANCELED,
            changed_by=request.user,
            comment="Отменено клиентом",
        )
        messages.success(request, "Бронирование отменено.")
    else:
        messages.error(request, "Эту бронь уже нельзя отменить.")

    return redirect("my_bookings")


staff_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff, login_url="login"
)


@staff_required
def admin_cars_list(request):
    """Показывает сотруднику страницу управления автомобилями."""
    cars = Car.objects.all().order_by("model_name")
    return render(request, "cars/admin_cars_list.html", {"cars": cars})


@staff_required
def admin_bookings_list(request):
    """Показывает сотруднику список броней с фильтрами и пагинацией."""
    bookings = (
        Booking.objects.select_related("car", "user")
        .prefetch_related("status_history__changed_by")
        .order_by(BOOKING_PRIORITY_ORDER, "-created_at")
    )

    q = (request.GET.get("q") or "").strip()
    status_filter = (request.GET.get("status") or "").strip()
    date_from = (request.GET.get("date_from") or "").strip()
    date_to = (request.GET.get("date_to") or "").strip()

    if q:
        bookings = bookings.filter(
            Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(car__model_name__icontains=q)
            | Q(id__icontains=q)
        )
    valid_statuses = {choice[0] for choice in BookingStatus.choices}
    if status_filter in valid_statuses:
        bookings = bookings.filter(status=status_filter)
    if date_from:
        dt_from = parse_datetime(f"{date_from}T00:00:00")
        if dt_from:
            bookings = bookings.filter(start_at__gte=dt_from)
    if date_to:
        dt_to = parse_datetime(f"{date_to}T23:59:59")
        if dt_to:
            bookings = bookings.filter(start_at__lte=dt_to)

    paginator = Paginator(bookings, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "cars/admin_bookings_list.html",
        {
            "bookings": page_obj.object_list,
            "page_obj": page_obj,
            "status_choices": BookingStatus.choices,
            "filters": {
                "q": q,
                "status": status_filter,
                "date_from": date_from,
                "date_to": date_to,
            },
        },
    )


@staff_required
def admin_booking_confirm(request, booking_id):
    """Переводит бронь из статуса created в confirmed."""
    if request.method != "POST":
        return redirect("admin_bookings_list")

    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status != BookingStatus.CREATED:
        messages.error(
            request,
            "Подтверждать можно только новые бронирования со статусом 'Создано'.",
        )
        return redirect("admin_bookings_list")

    previous_status = booking.status
    booking.status = BookingStatus.CONFIRMED
    booking.save(update_fields=["status"])
    _add_status_history(
        booking=booking,
        from_status=previous_status,
        to_status=BookingStatus.CONFIRMED,
        changed_by=request.user,
        comment="Подтверждено менеджером",
    )
    messages.success(request, f"Бронь #{booking.id} подтверждена менеджером.")
    return redirect("admin_bookings_list")


@staff_required
def admin_booking_cancel(request, booking_id):
    """Отменяет новую бронь с обязательным комментарием менеджера."""
    if request.method != "POST":
        return redirect("admin_bookings_list")

    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status != BookingStatus.CREATED:
        messages.error(
            request, "Отменять можно только новые бронирования со статусом 'Создано'."
        )
        return redirect("admin_bookings_list")

    manager_comment = (request.POST.get("manager_comment") or "").strip()
    if not manager_comment:
        messages.error(request, "Укажите причину отмены для клиента.")
        return redirect("admin_bookings_list")

    previous_status = booking.status
    booking.status = BookingStatus.CANCELED
    booking.manager_comment = manager_comment
    booking.save(update_fields=["status", "manager_comment"])
    _add_status_history(
        booking=booking,
        from_status=previous_status,
        to_status=BookingStatus.CANCELED,
        changed_by=request.user,
        comment=manager_comment,
    )
    messages.success(request, f"Бронь #{booking.id} отменена менеджером.")
    return redirect("admin_bookings_list")


@staff_required
def admin_booking_complete(request, booking_id):
    """Завершает подтвержденную бронь."""
    if request.method != "POST":
        return redirect("admin_bookings_list")

    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status != BookingStatus.CONFIRMED:
        messages.error(request, "Завершать можно только подтвержденные бронирования.")
        return redirect("admin_bookings_list")

    previous_status = booking.status
    booking.status = BookingStatus.COMPLETED
    booking.save(update_fields=["status"])
    _add_status_history(
        booking=booking,
        from_status=previous_status,
        to_status=BookingStatus.COMPLETED,
        changed_by=request.user,
        comment="Завершено менеджером",
    )
    messages.success(request, f"Бронь #{booking.id} завершена.")
    return redirect("admin_bookings_list")


@staff_required
def admin_car_create(request):
    """Создает новый автомобиль из панели сотрудника."""
    if request.method == "POST":
        form = CarManageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Автомобиль добавлен.")
            return redirect("admin_cars_list")
    else:
        form = CarManageForm()
    return render(
        request,
        "cars/admin_car_form.html",
        {"form": form, "page_title": "Добавить автомобиль"},
    )


@staff_required
def admin_car_edit(request, car_id):
    """Редактирует существующий автомобиль из панели сотрудника."""
    car = get_object_or_404(Car, pk=car_id)
    if request.method == "POST":
        form = CarManageForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Автомобиль обновлен.")
            return redirect("admin_cars_list")
    else:
        form = CarManageForm(instance=car)
    return render(
        request,
        "cars/admin_car_form.html",
        {"form": form, "page_title": "Редактировать автомобиль", "car": car},
    )


@staff_required
def admin_car_delete(request, car_id):
    """Удаляет автомобиль из панели сотрудника."""
    if request.method == "POST":
        car = get_object_or_404(Car, pk=car_id)
        car.delete()
        messages.success(request, "Автомобиль удален.")
    return redirect("admin_cars_list")


@staff_required
def admin_users_list(request):
    """Показывает сотруднику список пользователей."""
    users = get_user_model().objects.all().order_by("username")
    return render(request, "cars/admin_users_list.html", {"users": users})


@staff_required
def admin_user_create(request):
    """Создает нового пользователя из панели сотрудника."""
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь создан.")
            return redirect("admin_users_list")
    else:
        form = UserCreateForm()
    return render(
        request,
        "cars/admin_user_form.html",
        {"form": form, "page_title": "Добавить пользователя"},
    )


@staff_required
def admin_user_edit(request, user_id):
    """Редактирует профиль пользователя и его роль."""
    user_obj = get_object_or_404(get_user_model(), pk=user_id)
    if request.method == "POST":
        form = UserManageForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь обновлен.")
            return redirect("admin_users_list")
    else:
        form = UserManageForm(instance=user_obj)
    return render(
        request,
        "cars/admin_user_form.html",
        {
            "form": form,
            "page_title": "Редактировать пользователя",
            "user_obj": user_obj,
        },
    )


@staff_required
def admin_user_password(request, user_id):
    """Меняет пароль выбранного пользователя из панели сотрудника."""
    user_obj = get_object_or_404(get_user_model(), pk=user_id)
    if request.method == "POST":
        form = UserPasswordChangeForm(user_obj, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пароль обновлен.")
            return redirect("admin_users_list")
    else:
        form = UserPasswordChangeForm(user_obj)
    return render(
        request, "cars/admin_user_password.html", {"form": form, "user_obj": user_obj}
    )


@staff_required
def admin_user_delete(request, user_id):
    """Удаляет пользователя, кроме текущего авторизованного сотрудника."""
    if request.method == "POST":
        user_obj = get_object_or_404(get_user_model(), pk=user_id)
        if user_obj.pk == request.user.pk:
            messages.error(request, "Нельзя удалить текущего пользователя.")
            return redirect("admin_users_list")
        user_obj.delete()
        messages.success(request, "Пользователь удален.")
    return redirect("admin_users_list")
