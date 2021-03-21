from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sitemaps.views import sitemap

from blog.views import AboutView, handler404, handler500
from write_blog.views import image_upload
from blog.sitemaps import PostSitemap, CategorySitemap

sitemaps = {
    'post': PostSitemap,
    'category': CategorySitemap
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('user/', include('registration.urls')),
    path('profile/', include('user_profile.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('media/images/uploads/', csrf_exempt(image_upload)),
    path('', include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = handler404
handler500 = handler500
