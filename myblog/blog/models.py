from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Модель постов"""
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)
    title = models.CharField('Заголовок', max_length=250, db_index=True)
    slug = models.SlugField('url', max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='posts')
    body = models.TextField('Содержание', blank=True)
    publish = models.DateTimeField('Дата публикации', default=timezone.now)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата редактирования', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
