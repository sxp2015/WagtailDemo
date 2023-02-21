from django.db import models
from django.utils import timezone
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.fields import ParentalKey


# Create your models here.

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


class BlogPage(Page):
    date = models.DateField(verbose_name='发表日期', default=timezone.now)
    intro = models.CharField(verbose_name='内容介绍', max_length=250, blank=True)
    body = RichTextField(verbose_name='内容详情', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


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
