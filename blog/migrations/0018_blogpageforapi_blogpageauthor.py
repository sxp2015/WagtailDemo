# Generated by Django 4.1.2 on 2023-02-23 01:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0077_alter_revision_user'),
        ('wagtailimages', '0024_index_image_file_hash'),
        ('blog', '0017_alter_blogpage_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageForAPI',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('published_date', models.DateTimeField()),
                ('body', wagtail.fields.RichTextField()),
                ('private_field', models.CharField(max_length=255)),
                ('feed_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='作者名称')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='blog.blogpage', verbose_name='所属博客')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
