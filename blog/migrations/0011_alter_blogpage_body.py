# Generated by Django 4.1.2 on 2023-02-21 06:41

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blogpage_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True, verbose_name='内容详情'),
        ),
    ]