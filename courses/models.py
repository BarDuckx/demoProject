from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    birth_date = models.CharField(max_length=10, verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

class Application(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('learning', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    )
    TRANSPORT_CHOICES = (
        ('автобус', 'Автобус'),
        ('электробус', 'Электробус'),
        ('трамвай', 'Трамвай'),
    )
    PAYMENT_CHOICES = (
        ('qr', 'Предоплата по QR-коду'),
        ('mir', 'Оплата картой МИР'),
        ('office', 'Постоплата в офисе организации'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    transport_type = models.CharField(max_length=100, choices=TRANSPORT_CHOICES, verbose_name='Вид транспорта')
    start_date = models.CharField(max_length=10, verbose_name='Дата начала обучения')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    feedback = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']