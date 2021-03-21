from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from blog.models import Post, Categorie


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.update_date


class CategorySitemap(Sitemap):
    def items(self):
        return Categorie.objects.all()

# class StaticSitemap():
