from django.db import models
from django import forms
from django.utils import timezone
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from rest_framework.fields import DateField, DateTimeField


# Create your models here.

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    # 博客通常按时间倒序显示内容
    # 我们希望确保只显示已发布的内容。
    # 为了完成这些事情，我们需要做的不仅仅是在模板中抓取索引页的子页面。
    # 我们希望的是修改模型定义中的查询集。Wagtail通过重写的get_context（）
    # 方法来改变返回的默认列表
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        blog_pages = self.get_children().live().order_by('-first_published_at')
        context['blog_pages'] = blog_pages
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '博客分类'


class BlogPage(Page):
    date = models.DateField(verbose_name='发表日期', default=timezone.now)
    intro = models.CharField(verbose_name='内容介绍', max_length=250, blank=True)
    body = RichTextField(verbose_name='内容详情', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField(BlogCategory, blank=True, verbose_name='博客分类')

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    api_fields = [
        APIField('date'),
        APIField('intro'),
        APIField('body'),
        APIField('tags'),
        APIField('categories'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="博客信息"),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label="相册图片"),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


class BlogTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        # 过滤Tag
        tag = request.GET.get('tag')
        blog_pages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['blog_pages'] = blog_pages
        return context


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True,
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class BlogPageForAPI(Page):
    published_date = models.DateTimeField()
    body = RichTextField()
    feed_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True)
    private_field = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('body'),
        FieldPanel('feed_image'),
        FieldPanel('private_field'),

    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        blog_pages = self.get_children().live().order_by('-first_published_at')
        context['blog_pages'] = blog_pages
        return context

    # Export fields over the API
    api_fields = [
        APIField('published_date'),
        APIField('published_date_display', serializer=DateTimeField(format='%Y-%m-%d %H:%M:%S', source='published_date')),
        APIField('body'),
        APIField('feed_image'),
        APIField('authors'),  # This will nest the relevant BlogPageAuthor objects in the API response
    ]


class BlogPageAuthor(Orderable, Page):
    page = models.ForeignKey(BlogPageForAPI, on_delete=models.CASCADE, related_name='authors', verbose_name='所属博客')
    name = models.CharField(max_length=255, verbose_name='作者名称')
    content_panels = Page.content_panels + [
        FieldPanel('page'),
        FieldPanel('name')
    ]
    api_fields = [APIField('name')]
