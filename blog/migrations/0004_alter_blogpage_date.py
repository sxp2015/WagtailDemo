# Generated by Django 4.1.2 on 2023-02-21 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpage_date_alter_blogpage_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(blank=True, default='Y-m-d hh:mm:ss', verbose_name='发表日期'),
        ),
    ]
