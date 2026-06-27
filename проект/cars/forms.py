from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Booking, BookingStatus, Car


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "auth-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "auth-input"})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "auth-input"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "auth-input"})
        self.fields["password1"].widget.attrs.update({"class": "auth-input"})
        self.fields["password2"].widget.attrs.update({"class": "auth-input"})


class BookingCreateForm(forms.Form):
    """Форма создания брони в быстром или запланированном режиме."""

    mode = forms.ChoiceField(
        label="Режим бронирования",
        choices=[("quick", "Быстро"), ("planned", "Запланировать")],
        initial="quick",
        widget=forms.RadioSelect,
    )
    quick_duration = forms.ChoiceField(
        label="Длительность",
        choices=[
            ("30", "30 минут"),
            ("60", "1 час"),
            ("180", "3 часа"),
            ("360", "6 часов"),
            ("1440", "24 часа"),
        ],
        initial="60",
        widget=forms.Select(attrs={"class": "auth-input"}),
    )
    slot = forms.ChoiceField(
        label="Готовые слоты",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "auth-input"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.car = kwargs.pop("car")
        super().__init__(*args, **kwargs)
        self.slot_map = self._build_slots()
        self.fields["slot"].choices = [
            (key, value["label"]) for key, value in self.slot_map.items()
        ]
        if self.fields["slot"].choices:
            self.fields["slot"].initial = self.fields["slot"].choices[0][0]

    def _build_slots(self):
        """Генерирует ближайшие двухчасовые слоты для режима planned."""
        now = timezone.now().replace(second=0, microsecond=0)
        slots = {}
        for i in range(0, 16):
            start = (now + timedelta(hours=i)).replace(minute=0)
            end = start + timedelta(hours=2)
            key = f"{start.isoformat()}|{end.isoformat()}"
            slots[key] = {
                "start": start,
                "end": end,
                "label": f"{start:%d.%m %H:%M} - {end:%H:%M}",
            }
        return slots

    def clean(self):
        """Проверяет интервал времени и пересечения по выбранному авто."""
        cleaned_data = super().clean()
        mode = cleaned_data.get("mode")

        if mode == "quick":
            duration_minutes = int(cleaned_data.get("quick_duration", "60"))
            start_at = timezone.now() + timedelta(minutes=5)
            start_at = start_at.replace(second=0, microsecond=0)
            end_at = start_at + timedelta(minutes=duration_minutes)
        else:
            slot_key = cleaned_data.get("slot")
            if not slot_key or slot_key not in self.slot_map:
                raise forms.ValidationError("Выберите корректный слот.")
            start_at = self.slot_map[slot_key]["start"]
            end_at = self.slot_map[slot_key]["end"]

        if end_at <= start_at:
            raise forms.ValidationError("Окончание аренды должно быть позже начала.")
        if start_at < timezone.now():
            raise forms.ValidationError("Нельзя создавать бронь на прошедшее время.")

        has_conflict = Booking.objects.filter(
            car=self.car,
            status__in=[BookingStatus.CREATED, BookingStatus.CONFIRMED],
            start_at__lt=end_at,
            end_at__gt=start_at,
        ).exists()
        if has_conflict:
            raise forms.ValidationError(
                "Этот автомобиль уже забронирован на выбранный интервал."
            )

        cleaned_data["start_at"] = start_at
        cleaned_data["end_at"] = end_at
        return cleaned_data

    def save(self):
        """Сохраняет бронирование с уже проверенными датами."""
        return Booking.objects.create(
            user=self.user,
            car=self.car,
            start_at=self.cleaned_data["start_at"],
            end_at=self.cleaned_data["end_at"],
            status=BookingStatus.CREATED,
        )


class CarManageForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "model_name",
            "car_class",
            "year",
            "transmission",
            "seats",
            "price_per_hour",
            "description",
            "image_file",
            "is_active",
        ]
        widgets = {
            "model_name": forms.TextInput(attrs={"class": "auth-input"}),
            "car_class": forms.Select(attrs={"class": "auth-input"}),
            "year": forms.NumberInput(attrs={"class": "auth-input"}),
            "transmission": forms.Select(attrs={"class": "auth-input"}),
            "seats": forms.NumberInput(attrs={"class": "auth-input"}),
            "price_per_hour": forms.NumberInput(
                attrs={"class": "auth-input", "step": "0.01"}
            ),
            "description": forms.Textarea(attrs={"class": "auth-input", "rows": 4}),
            "image_file": forms.ClearableFileInput(attrs={"class": "auth-input"}),
        }


User = get_user_model()


ROLE_CHOICES = (
    ("client", "client"),
    ("manager", "manager"),
    ("admin", "admin"),
)


def _resolve_role_for_user(user):
    """Преобразует Django-флаги пользователя в значение роли формы."""
    if user.is_superuser:
        return "admin"
    if user.is_staff:
        return "manager"
    return "client"


def _apply_role_flags(user, role):
    """Применяет выбранную роль к флагам прав пользователя Django."""
    user.is_superuser = role == "admin"
    user.is_staff = role in {"admin", "manager"}


class UserManageForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "auth-input"}),
        label="Роль",
    )

    class Meta:
        model = User
        fields = ["username", "email", "role", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "auth-input"}),
            "email": forms.EmailInput(attrs={"class": "auth-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance
        if user and user.pk:
            self.fields["role"].initial = _resolve_role_for_user(user)

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data["role"]
        _apply_role_flags(user, role)
        if commit:
            user.save()
        return user


class UserCreateForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "auth-input"}),
        label="Роль",
    )
    email = forms.EmailField(
        required=False, widget=forms.EmailInput(attrs={"class": "auth-input"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "is_active")
        widgets = {
            "username": forms.TextInput(attrs={"class": "auth-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "auth-input"})
        self.fields["password1"].widget.attrs.update({"class": "auth-input"})
        self.fields["password2"].widget.attrs.update({"class": "auth-input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data["role"]
        _apply_role_flags(user, role)
        if commit:
            user.save()
        return user


class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "auth-input"})
        self.fields["new_password2"].widget.attrs.update({"class": "auth-input"})
