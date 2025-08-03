import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def get_upload_path(instance, filename):
    """
    Генерирует путь для загрузки файлов
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    
    # Определяем папку по типу модели
    model_name = instance.__class__.__name__.lower()
    return f"{model_name}/{filename}"


def get_image_upload_path(folder):
    """
    Возвращает функцию для загрузки изображений в определенную папку
    """
    def upload_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f"images/{folder}/{filename}"
    return upload_path


def create_slug(text, max_length=50):
    """
    Создает slug из текста
    """
    return slugify(text)[:max_length]


class LanguageChoices(models.TextChoices):
    """
    Выбор языков для многоязычного контента
    """
    ENGLISH = 'en', _('English')
    RUSSIAN = 'ru', _('Russian')
    HEBREW = 'he', _('Hebrew')