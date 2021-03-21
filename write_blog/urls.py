from django.urls import path

from .views import CreatePost

from compression_middleware.decorators import compress_page

app_name = 'write_blog'

urlpatterns = [
    path('write-post/', compress_page(CreatePost.as_view()), name='write_post')
]
