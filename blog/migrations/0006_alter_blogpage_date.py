# Generated by Django 4.1.2 on 2023-02-21 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpage_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(blank=True, default='YYYY-MM-DD', verbose_name='发表日期'),
        ),
    ]
