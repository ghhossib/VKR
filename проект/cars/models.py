from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:
    Image = None
    ImageOps = None
    UnidentifiedImageError = Exception


class CarClass(models.TextChoices):
    ECONOMY = "economy", "Эконом"
    COMFORT = "comfort", "Комфорт"
    BUSINESS = "business", "Бизнес"
    SUV = "suv", "SUV"


class TransmissionType(models.TextChoices):
    AUTOMATIC = "automatic", "Автомат"
    MANUAL = "manual", "Механика"


class BookingStatus(models.TextChoices):
    CREATED = "created", "Создано"
    CONFIRMED = "confirmed", "Подтверждено"
    COMPLETED = "completed", "Завершено"
    CANCELED = "canceled", "Отменено"


class Car(models.Model):
    """Сущность автомобиля, доступного для каталога и бронирования."""

    model_name = models.CharField("Модель", max_length=120)
    car_class = models.CharField("Класс", max_length=20, choices=CarClass.choices)
    year = models.PositiveIntegerField("Год")
    transmission = models.CharField(
        "Коробка", max_length=20, choices=TransmissionType.choices
    )
    seats = models.PositiveSmallIntegerField("Мест")
    price_per_hour = models.DecimalField("Цена/час", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    image_url = models.URLField("Изображение", blank=True)
    image_file = models.FileField(
        "Фото (загрузка)", upload_to="cars/", blank=True, null=True
    )
    is_active = models.BooleanField("Доступен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    IMAGE_MAX_SIZE = (1600, 1600)
    IMAGE_WEBP_QUALITY = 78

    class Meta:
        ordering = ["car_class", "-price_per_hour", "model_name"]

    def __str__(self) -> str:
        return self.model_name

    def save(self, *args, **kwargs):
        """Оптимизирует загруженное изображение перед сохранением модели."""
        self._optimize_uploaded_image()
        super().save(*args, **kwargs)

    def _optimize_uploaded_image(self):
        if not self.image_file or not Image:
            return

        try:
            self.image_file.seek(0)
            image = Image.open(self.image_file)
            image = ImageOps.exif_transpose(image)
            image.thumbnail(self.IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)

            # Сохраняем прозрачность, иначе используем RGB для лучшего сжатия.
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

            buffer = BytesIO()
            image.save(
                buffer,
                format="WEBP",
                quality=self.IMAGE_WEBP_QUALITY,
                method=6,
                optimize=True,
            )
            buffer.seek(0)

            original_stem = Path(self.image_file.name).stem
            new_name = f"{original_stem}.webp"
            self.image_file.save(new_name, ContentFile(buffer.read()), save=False)
        except (UnidentifiedImageError, OSError, ValueError, AttributeError):
            # Если оптимизация не удалась, оставляем исходный файл без изменений.
            return

    @property
    def display_image(self) -> str:
        if self.image_file:
            return self.image_file.url
        return self.image_url


class Booking(models.Model):
    """Заявка на бронирование автомобиля на конкретный период."""

    user = models.ForeignKey(
        "auth.User",
        related_name="bookings",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car,
        related_name="bookings",
        on_delete=models.PROTECT,
        verbose_name="Автомобиль",
    )
    start_at = models.DateTimeField("Начало аренды")
    end_at = models.DateTimeField("Окончание аренды")
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CREATED,
    )
    manager_comment = models.TextField("Комментарий менеджера", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self) -> str:
        return f"{self.user} - {self.car} ({self.start_at:%Y-%m-%d %H:%M})"

    def clean(self):
        if self.end_at <= self.start_at:
            raise ValueError("Время окончания должно быть позже времени начала.")
        if self.start_at < timezone.now():
            raise ValueError("Нельзя создать бронирование в прошлом.")

    @property
    def duration_hours(self) -> float:
        return (self.end_at - self.start_at).total_seconds() / 3600

    @property
    def total_price(self):
        return round(float(self.car.price_per_hour) * self.duration_hours, 2)


class BookingMessage(models.Model):
    """Сообщение в чате между клиентом и менеджером по брони."""

    booking = models.ForeignKey(
        Booking,
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name="Бронирование",
    )
    author = models.ForeignKey(
        "auth.User",
        related_name="booking_messages",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField("Сообщение", max_length=2000)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"#{self.booking_id} {self.author}: {self.text[:30]}"


class BookingStatusHistory(models.Model):
    """Журнал изменений статусов бронирования."""

    booking = models.ForeignKey(
        Booking,
        related_name="status_history",
        on_delete=models.CASCADE,
        verbose_name="Бронирование",
    )
    from_status = models.CharField(
        "Статус до", max_length=20, choices=BookingStatus.choices
    )
    to_status = models.CharField(
        "Статус после", max_length=20, choices=BookingStatus.choices
    )
    changed_by = models.ForeignKey(
        "auth.User",
        related_name="booking_status_changes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто изменил",
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"#{self.booking_id}: {self.from_status} -> {self.to_status}"
