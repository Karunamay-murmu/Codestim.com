import uuid
import json

from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.views import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page

from blog.models import Post, Categorie, Comment, Subscriber, Contact
from blog.forms import CommentForm, SubscriberForm, ContactForm
from registration.models import User

@method_decorator(compress_page, name="dispatch")
class AboutView(TemplateView):
    template_name = 'about.html'

@method_decorator(compress_page, name="dispatch")
class PrivacyPolicyView(TemplateView):
    template_name = 'privacyPolicy.html'

@method_decorator(compress_page, name="dispatch")
class TermsOfServiceView(TemplateView):
    template_name = 'termsOfService.html'

class Search(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET['query']
        all_posts = None

        if len(query) > 60 or len(query) == 0:
            posts = []
        else:
            post_by_title = Post.objects.filter(
                title__icontains=query)
            post_by_category = Post.objects.filter(
                category__name__icontains=query)
            post_by_tag = Post.objects.filter(tags__icontains=query)
            all_posts = post_by_title.union(post_by_category, post_by_tag)

        if all_posts:
            post_per_page = Paginator(all_posts, 10)
            page_number = self.request.GET.get('page')
            posts = post_per_page.get_page(page_number)
        else:
            posts = []

        return render(request, self.template_name, {'posts': posts, 'query': query})


class CategoryPost(TemplateView):
    template_name = 'blog/categoryPost.html'

    def get_context_data(self, **kwargs):
        category_name = self.kwargs['slug'].replace("-", " ")
        all_posts = Post.objects.all().filter(category__name__iexact=category_name).order_by('-publish_date')

        context = super().get_context_data(**kwargs)
        post_per_page = Paginator(all_posts, 15)

        page_number = self.request.GET.get('page')
        posts = post_per_page.get_page(page_number)

        context['category_name'] = category_name
        context['active'] = 'active'

        if posts:
            context['posts'] = posts
        else:
            context['no_post'] = True

        return context


class PostPageView(View):
    template_name = 'blog/postPage.html'
    

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        post = get_object_or_404(Post, slug__iexact=slug)
        related_category_post = Post.objects.filter(
           category__name__iexact=post.category).exclude(title__iexact=post.title)[:3]
        tags = post.tags.split(",")
        comments = Comment.objects.all().filter(post__postId=post.postId, isApprove=True)

        context_dict = {
            'post_tags': tags,
            'post': post,
            'related_category_post': related_category_post,
            'form': CommentForm(),
            'comments': comments
        }

        return render(request, self.template_name, context_dict)
    
    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        post = get_object_or_404(Post, slug__iexact=slug)
        form = CommentForm(request.POST or None)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            messages.info(
                request, 'Your comment is awaiting moderation', extra_tags='info')

            return redirect(request.path)
  
        if request.body:
            data = json.loads(request.body.decode("utf-8"))
            post = Post.objects.get(postId=data['postid'])
            post.liked += 1

            post.save()

            return JsonResponse({'likes': post.liked})
           

        return HttpResponseRedirect(request.path)

class Home(View):
    def get(self, request, *args, **kwargs):

        categories = Categorie.objects.all()
        posts = Post.objects.all().order_by('-publish_date')

        context = {}
        category_list = []

        for category in categories:
            category_posts = Post.objects.all().filter(
                category__name__iexact=category).order_by('-publish_date')[:6]

            category_name = category.name.replace(" ", "")\
                if category.name.find(" ")\
                else category

            category_list.append({
                "posts": category_posts,
                "obj": category
            })

        context['categories'] = category_list
        context['posts'] = posts
        context['has_data'] = True

        if not posts:
            context['has_data'] = False

        return render(request, 'blog/home.html', context)


class ContactFormView(CreateView):
    form_class = ContactForm
    template_name = 'contact.html'

    def form_valid(self, form):
        path = self.request.path
        is_contact_path = ('/contact/' == path)
        feedback_message_identifier = "contact with us" if is_contact_path else "feedback"

        form_data = form.save(commit=False)
        form_data.message_type = path[1:len(path) - 1]
        form_data.save()

        messages.info(
            self.request, f"Thank you for {feedback_message_identifier}. You'll recive a email from us shortly", extra_tags='info')

        return super().form_valid(form)


class EmailSubscription(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('subscriber_email')
        if email:
            subs = Subscriber(subscriber_email=email)
            subs.save()

            messages.info(
                self.request, "Thank you for subscribe our newsletter", extra_tags='success')

        return redirect(request.GET['next'])


def handler404(request, exception):
    error_text = 'The link is broken or the page has been removed.'
    return render(
        request,
        'error.html',
        {
            'error_code': '404',
            'error_text': error_text
        },
        status=404
    )


def handler500(request):
    error_text = 'Something went wrong to the server.'
    return render(
        request,
        'error.html',
        {
            'error_code': '500',
            'error_text': error_text
        },
        status=500
    )
