from django.utils import timezone
from rest_framework import serializers

from .models import Booking, BookingStatus, Car


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор автомобиля для публичного API."""

    class Meta:
        model = Car
        fields = [
            "id",
            "model_name",
            "car_class",
            "year",
            "transmission",
            "seats",
            "price_per_hour",
            "description",
            "image_url",
            "is_active",
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор бронирования с проверкой интервала и пересечений."""

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "car",
            "start_at",
            "end_at",
            "status",
            "created_at",
            "total_price",
        ]
        read_only_fields = ["status", "created_at"]

    def get_total_price(self, obj):
        """Возвращает итоговую стоимость бронирования."""
        return obj.total_price

    def validate(self, attrs):
        """Проверяет корректность дат и отсутствие конфликтов по автомобилю."""
        car = attrs.get("car")
        start_at = attrs.get("start_at")
        end_at = attrs.get("end_at")

        if end_at <= start_at:
            raise serializers.ValidationError(
                "Окончание аренды должно быть позже начала."
            )
        if start_at < timezone.now():
            raise serializers.ValidationError(
                "Нельзя создавать бронь на прошедшее время."
            )

        conflicts = Booking.objects.filter(
            car=car,
            status__in=[BookingStatus.CREATED, BookingStatus.CONFIRMED],
            start_at__lt=end_at,
            end_at__gt=start_at,
        )

        if self.instance:
            conflicts = conflicts.exclude(pk=self.instance.pk)

        if conflicts.exists():
            raise serializers.ValidationError(
                "Этот автомобиль уже забронирован на выбранный интервал."
            )

        return attrs

    def create(self, validated_data):
        """Автоматически привязывает создаваемую бронь к текущему пользователю."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
