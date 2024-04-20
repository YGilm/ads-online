from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}


class Ad(models.Model):
    """
    Модель объявления, содержащая информацию о товаре, включая название, цену,
    описание, автора объявления и время создания.
    """
    title = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='ads_images/', verbose_name='Изображение', **NULLABLE, )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор', related_name='ads')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Модель отзыва, содержащая текст отзыва, автора отзыва, связь с объявлением,
    и дату создания. Отзывы предоставляют обратную связь на объявления.
    """
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор',
                               related_name='reviews')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление', related_name='reviews')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author} создан: {self.created_at}"
