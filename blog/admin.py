from django.contrib import admin
from blog.models import Post, Comment, Categorie, Tag, Draft, Contact, Subscriber
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Categorie)
admin.site.register(Tag)
admin.site.register(Draft)
admin.site.register(Contact)
admin.site.register(Subscriber)
