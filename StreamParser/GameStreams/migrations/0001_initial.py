# Generated by Django 3.0.6 on 2020-05-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('folder', models.TextField(verbose_name='Каталог')),
                ('duration', models.TextField(verbose_name='Длительность видео')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата парсинга')),
                ('channel', models.TextField(verbose_name='Канал')),
                ('name', models.TextField(verbose_name='Название')),
                ('platform', models.TextField(default='YouTube', verbose_name='Платформа')),
            ],
        ),
    ]
