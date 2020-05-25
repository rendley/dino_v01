from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from slugify import slugify
from time import time


class Post(models.Model):
    """Модель постов"""
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)
    title = models.CharField('Заголовок', max_length=250, db_index=True)
    slug = models.SlugField('url', max_length=250, unique=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='posts')
    body = models.TextField('Содержание', blank=True)
    publish = models.DateTimeField('Дата публикации', default=timezone.now)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата редактирования', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='published')

    def save(self, *args, **kwargs):
        # unique slug unicode
        slug = slugify(self.title)
        unique_slug = slug + '-' + str(int(time()))
        self.slug = unique_slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментариев"""
    post = models.ForeignKey(Post, verbose_name='Статья', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='comments')
    body = models.TextField('Содержание', )
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    active = models.BooleanField('Модерация', default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Комментарий {self.body}, поста {self.post}.'

