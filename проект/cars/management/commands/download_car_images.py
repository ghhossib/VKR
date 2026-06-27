"""Скачивает внешние изображения автомобилей и сохраняет их локально.

Команда проходит по всем машинам, у которых задан ``image_url`` и нет
``image_file``, скачивает картинку, прогоняет её через ту же оптимизацию,
что используется в ``Car.save`` (EXIF + thumbnail 1600x1600 + WEBP), и
привязывает готовый файл к полю ``image_file``. После этого объявление
отображается с локальной картинкой, а не по внешней ссылке.

Запуск::

    python manage.py download_car_images
    python manage.py download_car_images --force   # перекачать даже те, где файл уже есть
"""

from __future__ import annotations

import time
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from cars.models import Car

try:
    import requests
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError as exc:  # pragma: no cover
    raise CommandError(
        "Для работы команды нужны библиотеки requests и Pillow: "
        "pip install requests Pillow"
    ) from exc


class Command(BaseCommand):
    help = "Скачивает внешние изображения автомобилей в media/cars/ как локальные WEBP-файлы."

    DEFAULT_TIMEOUT = 20
    USER_AGENT = (
        "Mozilla/5.0 (compatible; SHDDriveBot/1.0; +local image cache for car cards)"
    )
    # Пауза между запросами, чтобы хосты вроде Wikimedia не отдавали 429.
    REQUEST_DELAY = 1.0
    MAX_RETRIES = 3

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Перекачать фото даже для машин, у которых image_file уже задан.",
        )

    def handle(self, *args, force: bool = False, **options):
        cars = Car.objects.all().order_by("id")
        if not cars.exists():
            self.stdout.write("Машин в базе нет — нечего скачивать.")
            return

        success = skipped = failed = 0
        for car in cars:
            if not force and car.image_file:
                self.stdout.write(
                    self.style.WARNING(
                        f"[skip] #{car.id} {car.model_name}: уже есть локальный файл "
                        f"({car.image_file.name})"
                    )
                )
                skipped += 1
                continue

            if not car.image_url:
                self.stdout.write(
                    self.style.WARNING(
                        f"[skip] #{car.id} {car.model_name}: нет image_url"
                    )
                )
                skipped += 1
                continue

            try:
                content = self._fetch(car.image_url)
                file_name = self._build_name(car, car.image_url)
                self._save_optimized(car, file_name, content)
            except Exception as exc:  # noqa: BLE001 - хотим видеть любую ошибку
                self.stderr.write(
                    self.style.ERROR(
                        f"[fail] #{car.id} {car.model_name}: {exc}"
                    )
                )
                failed += 1
                continue

            self.stdout.write(
                self.style.SUCCESS(
                    f"[ok]   #{car.id} {car.model_name}: {car.image_file.name}"
                )
            )
            success += 1
            time.sleep(self.REQUEST_DELAY)

        self.stdout.write(
            self.style.NOTICE(
                f"\nГотово. Скачано: {success}, пропущено: {skipped}, ошибок: {failed}."
            )
        )

    # ------------------------------------------------------------------ helpers

    def _fetch(self, url: str) -> bytes:
        """Качает картинку по URL с повторами при 429/5xx.

        Поддерживает редиректы Wikimedia. Между попытками ждём с возрастающей
        задержкой, чтобы не провоцировать rate-limiting.
        """
        last_error: Exception | None = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = requests.get(
                    url,
                    timeout=self.DEFAULT_TIMEOUT,
                    headers={"User-Agent": self.USER_AGENT},
                    allow_redirects=True,
                )
                if response.status_code == 429 or response.status_code >= 500:
                    raise requests.HTTPError(
                        f"{response.status_code} {response.reason}", response=response
                    )
                response.raise_for_status()
                return response.content
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < self.MAX_RETRIES:
                    backoff = self.REQUEST_DELAY * attempt
                    self.stdout.write(
                        self.style.WARNING(
                            f"  повтор {attempt + 1}/{self.MAX_RETRIES} через "
                            f"{backoff:.0f}с ({exc})"
                        )
                    )
                    time.sleep(backoff)
        raise last_error  # type: ignore[misc]

    def _save_optimized(self, car: Car, file_name: str, content: bytes) -> None:
        """Оптимизирует картинку и кладёт её в media/cars/<file_name>.

        Пишем напрямую в storage и обновляем строку через QuerySet.update — так
        мы НЕ вызываем Car.save() и избегаем повторной оптимизации, которая в
        Car.save переименовывает файл и навешивает случайный суффикс. Имя файла
        остаётся чистым и детерминированным: <slug-модели>.webp.
        """
        image = Image.open(BytesIO(content))
        image = ImageOps.exif_transpose(image)
        image.thumbnail(Car.IMAGE_MAX_SIZE, Image.Resampling.LANCZOS)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

        buffer = BytesIO()
        image.save(
            buffer,
            format="WEBP",
            quality=Car.IMAGE_WEBP_QUALITY,
            method=6,
            optimize=True,
        )

        storage_path = f"cars/{file_name}"
        # Если файл с таким именем уже есть (повторный запуск, --force),
        # storage.save добавил бы суффикс — поэтому удаляем и пишем заново.
        if default_storage.exists(storage_path):
            default_storage.delete(storage_path)
        saved_path = default_storage.save(storage_path, ContentFile(buffer.getvalue()))
        Car.objects.filter(pk=car.pk).update(image_file=saved_path)
        # Обновляем объект в памяти, чтобы корректно вывести имя в логе.
        car.image_file.name = saved_path
        car.refresh_from_db()

    @staticmethod
    def _build_name(car: Car, url: str) -> str:
        """Детерминированное имя файла по модели автомобиля.

        Используем model_name (например 'Porsche Macan' -> 'porsche-macan'),
        чтобы имя не зависело от внешнего URL и было стабильным при повторных
        запусках. URL оставлен в сигнатуре только для совместимости.
        """
        slug = "".join(
            ch if ch.isalnum() else "-" for ch in (car.model_name or "").lower()
        )
        slug = "-".join(part for part in slug.split("-") if part)
        if not slug:
            # запасной вариант — разбираем URL
            stem = Path(unquote(urlparse(url).path)).stem or f"car-{car.id}"
            slug = "".join(ch if ch.isalnum() else "-" for ch in stem.lower())
            slug = "-".join(part for part in slug.split("-") if part)
        return f"{slug}.webp"
