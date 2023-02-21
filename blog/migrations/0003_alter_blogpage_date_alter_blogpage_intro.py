# Generated by Django 4.1.2 on 2023-02-21 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(blank=True, verbose_name='发表日期'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='intro',
            field=models.CharField(blank=True, max_length=250, verbose_name='内容介绍'),
        ),
    ]