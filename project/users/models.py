from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('common', 'Общий конкурс'),
        ('target', 'Целевое'),
        ('special', 'Особая квота'),
        ('no_exam', 'Без вступительных'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    score = models.FloatField(null=True, blank=True, verbose_name='Ваши баллы')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='common', verbose_name='Ваш статус')

    def __str__(self):
        return f"{self.user.username} – {self.score} баллов"