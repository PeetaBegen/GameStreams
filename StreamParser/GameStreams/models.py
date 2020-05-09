from django.db import models


class Stream(models.Model):
    url = models.URLField(verbose_name='URL')
    folder = models.TextField(verbose_name='Каталог')
    duration = models.TextField(verbose_name='Длительность видео')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата парсинга')
    channel = models.TextField(verbose_name='Канал')
    name = models.TextField(verbose_name='Название')
    platform = models.TextField(verbose_name='Платформа', default='YouTube')
