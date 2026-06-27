from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Booking, Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Настройки отображения и редактирования автомобилей в Django Admin."""

    list_display = (
        "model_name",
        "car_class",
        "year",
        "price_per_hour",
        "is_active",
        "image_preview",
    )
    list_filter = ("car_class", "is_active", "transmission")
    search_fields = ("model_name",)
    fields = (
        "model_name",
        "car_class",
        "year",
        "transmission",
        "seats",
        "price_per_hour",
        "description",
        "image_url",
        "image_file",
        "image_preview",
        "is_active",
    )
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """Показывает миниатюру изображения автомобиля в админке."""
        if not obj:
            return "Сохраните объект, чтобы увидеть предпросмотр."
        image = obj.display_image
        if not image:
            return "Фото не загружено."
        return mark_safe(
            f'<img src="{image}" style="height:80px;width:140px;object-fit:cover;border:1px solid #ddd;" />'
        )

    image_preview.short_description = "Предпросмотр"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Настройки отображения бронирований в Django Admin."""

    list_display = ("id", "user", "car", "start_at", "end_at", "status")
    list_filter = ("status", "car__car_class")
    search_fields = ("user__username", "car__model_name")
