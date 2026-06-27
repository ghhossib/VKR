from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, BookingStatus, BookingStatusHistory, Car


class BookingApiTests(APITestCase):
    """Тесты API бронирований: создание и проверка конфликтов интервалов."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345"
        )
        self.car = Car.objects.create(
            model_name="Test Car",
            car_class="comfort",
            year=2024,
            transmission="automatic",
            seats=5,
            price_per_hour=1000,
            is_active=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_booking_success(self):
        start_at = timezone.now() + timedelta(hours=2)
        end_at = start_at + timedelta(hours=3)

        response = self.client.post(
            "/api/bookings/",
            {
                "car": self.car.id,
                "start_at": start_at.isoformat(),
                "end_at": end_at.isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_overlap_rejected(self):
        start_at = timezone.now() + timedelta(hours=2)
        end_at = start_at + timedelta(hours=3)
        Booking.objects.create(
            user=self.user,
            car=self.car,
            start_at=start_at,
            end_at=end_at,
            status=BookingStatus.CONFIRMED,
        )

        response = self.client.post(
            "/api/bookings/",
            {
                "car": self.car.id,
                "start_at": (start_at + timedelta(hours=1)).isoformat(),
                "end_at": (end_at + timedelta(hours=1)).isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("уже забронирован", str(response.data))


class BookingWebFlowTests(TestCase):
    """Интеграционные тесты веб-сценариев клиента и менеджера."""

    def setUp(self):
        User = get_user_model()
        self.client_user = User.objects.create_user(
            username="client1", password="test12345", email="c@example.com"
        )
        self.other_user = User.objects.create_user(
            username="client2", password="test12345", email="o@example.com"
        )
        self.manager = User.objects.create_user(
            username="manager1", password="test12345", is_staff=True
        )
        self.car = Car.objects.create(
            model_name="Toyota Camry",
            car_class="comfort",
            year=2023,
            transmission="automatic",
            seats=5,
            price_per_hour=1800,
            is_active=True,
        )
        start_at = timezone.now() + timedelta(hours=3)
        self.booking = Booking.objects.create(
            user=self.client_user,
            car=self.car,
            start_at=start_at,
            end_at=start_at + timedelta(hours=2),
            status=BookingStatus.CONFIRMED,
        )
        self.web_client = Client()

    def test_manager_can_complete_confirmed_booking_and_history_created(self):
        self.web_client.login(username="manager1", password="test12345")
        response = self.web_client.post(
            f"/dashboard/bookings/{self.booking.id}/complete/"
        )
        self.assertEqual(response.status_code, 302)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, BookingStatus.COMPLETED)
        history = BookingStatusHistory.objects.filter(booking=self.booking).latest(
            "created_at"
        )
        self.assertEqual(history.from_status, BookingStatus.CONFIRMED)
        self.assertEqual(history.to_status, BookingStatus.COMPLETED)

    def test_chat_access_forbidden_for_other_client(self):
        self.web_client.login(username="client2", password="test12345")
        response = self.web_client.get(f"/my-bookings/{self.booking.id}/chat/messages/")
        self.assertEqual(response.status_code, 403)

    def test_manager_bookings_list_filter_and_pagination(self):
        self.web_client.login(username="manager1", password="test12345")

        for idx in range(12):
            Booking.objects.create(
                user=self.client_user,
                car=self.car,
                start_at=timezone.now() + timedelta(days=idx + 1),
                end_at=timezone.now() + timedelta(days=idx + 1, hours=2),
                status=BookingStatus.CREATED,
            )

        filtered = self.web_client.get("/dashboard/bookings/", {"status": "confirmed"})
        self.assertEqual(filtered.status_code, 200)
        self.assertContains(filtered, "Подтверждено")

        paged = self.web_client.get("/dashboard/bookings/", {"page": 2})
        self.assertEqual(paged.status_code, 200)
        self.assertContains(paged, "Страница")
