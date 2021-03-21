from django.urls import path, include

from .views import (
    Home,
    CategoryPost,
    PostPageView,
    ContactFormView,
    EmailSubscription,
    AboutView,
    PrivacyPolicyView,
    TermsOfServiceView,
    Search,
)
from blog.models import Post, Categorie, Comment
from write_blog.views import EditOrPublishDraft, EditOrSwitchPostToDraft

from compression_middleware.decorators import compress_page

app_name = 'blog'

urlpatterns = [
    path('', compress_page(Home.as_view()), name='home'),
    path('search', compress_page(Search.as_view()), name='search'),
    path('category/<slug:slug>',
         compress_page(CategoryPost.as_view()), name='category'),
    path('post/<str:id>/<slug:slug>/edit-post',
         compress_page(EditOrSwitchPostToDraft.as_view()), name='edit-post'),
    path('draft/<str:id>/edit-draft',
         compress_page(EditOrPublishDraft.as_view()), name='edit-or-publish-draft'),
    path('report/', compress_page(ContactFormView.as_view()), name='report'),
    path('contact/', compress_page(ContactFormView.as_view()), name='contact'),
    path('subscribe/', compress_page(EmailSubscription.as_view()), name='subscribe'),
    path('about/', compress_page(AboutView.as_view()), name='about'),
    path('privacy-policy/', compress_page(PrivacyPolicyView.as_view()),
         name='privacy_policy'),
    path('terms-of-service/',
         compress_page(TermsOfServiceView.as_view()), name='terms'),
    path('<slug:slug>', compress_page(PostPageView.as_view()), name='post_detail'),
]
