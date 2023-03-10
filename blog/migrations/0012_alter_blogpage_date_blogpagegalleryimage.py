# Generated by Django 4.1.2 on 2023-02-21 08:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('blog', '0011_alter_blogpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='发表日期'),
        ),
        migrations.CreateModel(
            name='BlogPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='blog.blogpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
