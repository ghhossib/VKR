from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .forms import StyledAuthenticationForm
from .views import (
    BookingViewSet,
    CarViewSet,
    admin_booking_cancel,
    admin_booking_complete,
    admin_booking_confirm,
    admin_bookings_list,
    admin_car_create,
    admin_car_delete,
    admin_car_edit,
    admin_cars_list,
    admin_user_create,
    admin_user_delete,
    admin_user_edit,
    admin_user_password,
    admin_users_list,
    booking_chat,
    booking_chat_messages,
    cancel_booking,
    car_detail,
    landing_page,
    my_bookings,
    register_view,
)

# DRF-роутер для API автомобилей и бронирований.
router = DefaultRouter()
router.register("cars", CarViewSet, basename="cars")
router.register("bookings", BookingViewSet, basename="bookings")

urlpatterns = [
    path("", landing_page, name="landing"),
    path("register/", register_view, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="cars/login.html",
            authentication_form=StyledAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="landing"), name="logout"),
    path("cars/<int:car_id>/", car_detail, name="car_detail"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("my-bookings/<int:booking_id>/chat/", booking_chat, name="booking_chat"),
    path(
        "my-bookings/<int:booking_id>/chat/messages/",
        booking_chat_messages,
        name="booking_chat_messages",
    ),
    path("my-bookings/<int:booking_id>/cancel/", cancel_booking, name="cancel_booking"),
    path("dashboard/cars/", admin_cars_list, name="admin_cars_list"),
    path("dashboard/bookings/", admin_bookings_list, name="admin_bookings_list"),
    path(
        "dashboard/bookings/<int:booking_id>/confirm/",
        admin_booking_confirm,
        name="admin_booking_confirm",
    ),
    path(
        "dashboard/bookings/<int:booking_id>/cancel/",
        admin_booking_cancel,
        name="admin_booking_cancel",
    ),
    path(
        "dashboard/bookings/<int:booking_id>/complete/",
        admin_booking_complete,
        name="admin_booking_complete",
    ),
    path("dashboard/cars/create/", admin_car_create, name="admin_car_create"),
    path("dashboard/cars/<int:car_id>/edit/", admin_car_edit, name="admin_car_edit"),
    path(
        "dashboard/cars/<int:car_id>/delete/", admin_car_delete, name="admin_car_delete"
    ),
    path("dashboard/users/", admin_users_list, name="admin_users_list"),
    path("dashboard/users/create/", admin_user_create, name="admin_user_create"),
    path(
        "dashboard/users/<int:user_id>/edit/", admin_user_edit, name="admin_user_edit"
    ),
    path(
        "dashboard/users/<int:user_id>/password/",
        admin_user_password,
        name="admin_user_password",
    ),
    path(
        "dashboard/users/<int:user_id>/delete/",
        admin_user_delete,
        name="admin_user_delete",
    ),
    path("api/", include(router.urls)),
]
