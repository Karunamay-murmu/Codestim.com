from django.urls import path, include

from .views import (
    Dashboard,
    Posts,
    Drafts,
    Comments,
    EditProfile,
    ProfileInfo,
    Search
)

from compression_middleware.decorators import compress_page

app_name = 'dashboard'

urlpatterns = [
    path('<str:user>/<str:id>/',
         compress_page(ProfileInfo.as_view()), name='profileInfo'),
    path('<str:user>/<str:id>/posts',
         compress_page(Posts.as_view()), name='posts'),
    path('<str:user>/<str:id>/drafts',
         compress_page(Drafts.as_view()), name='drafts'),
    path('<str:user>/<str:id>/comments',
         compress_page(Comments.as_view()), name='comments'),
    path('<str:user>/<str:id>/edit-profile',
         compress_page(EditProfile.as_view()), name='editProfile'),
    path('<str:user>/<str:id>/search',
         compress_page(Search.as_view()), name='search'),
    path('<str:user>/<str:id>/', include('write_blog.urls'))
]
