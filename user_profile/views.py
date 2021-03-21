import uuid
import re

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.paginator import Paginator
from compression_middleware.decorators import compress_page
from django.views.decorators.cache import never_cache

from registration.models import User
from blog.models import Post, Comment, Draft
from .forms import EditProfileForm
from write_blog.forms import postForm


@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class Dashboard(LoginRequiredMixin, View):
    template_name = 'user_profile/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        logged_user = request.user
        if kwargs['user'] != logged_user.username or kwargs['id'] != str(logged_user.userId):
            return HttpResponseForbidden("You are not authenticated to access this page")

        return super(Dashboard, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(args)
        return render(request, self.template_name)

@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class Posts(Dashboard):
    template_name = 'user_profile/posts.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(authorId=kwargs['id'])

        return render(request, self.template_name, {'posts': posts, 'model': 'post'})

    def post(self, request, *args, **kwargs):
        '''
        Handle POST method to delete posts
        '''
        user = request.user
        _id = request.POST.get('id')

        if _id:
            post = get_object_or_404(Post, postId=_id)
            post.delete()

        return redirect(request.path)

@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class Drafts(Dashboard):
    template_name = 'user_profile/drafts.html'

    def get(self, request, *args, **kwargs):
        drafts = Draft.objects.filter(authorId=kwargs['id'])

        return render(request, self.template_name, {'drafts': drafts, 'model': 'draft'})

    def post(self, request, *args, **kwargs):
        '''
        Handle POST method to delete drafts
        '''
        _id = request.POST.get('id')
        if _id:
            post = get_object_or_404(Draft, postId=_id)
            post.delete()

        return redirect(request.path)

@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class Comments(Dashboard):
    template_name = 'user_profile/comments.html'

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all().filter(
            post__authorId=self.kwargs['id'])

        '''
        Delete or approve comment
        '''
        _id = request.GET.get('id')
        if _id:
            comment = get_object_or_404(Comment, commentId=_id)
            if request.GET.get('action') == 'delete':
                comment.delete()
                messages.info(request, 'comment deleted')

                return redirect(request.path)

            else:
                approve = comment.approveOrDisapprove()
                messages.info(
                    request, 'Comment Approved' if approve else 'Comment Disapprove', extra_tags='info')

                return redirect(request.path)

        return render(request, self.template_name, {'comments': comments, 'model': 'comment'})

@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class ProfileInfo(Dashboard):
    template_name = 'user_profile/profileInfo.html'

    def get(self, request, *args, **kwargs):
        profile = User.objects.get(userId=request.user.userId)

        return render(request, self.template_name, {'profile': profile})

@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'user_profile/editProfile.html'

    def dispatch(self, request, **kwargs):
        logged_user = request.user
        if logged_user.username != kwargs['user'] or str(logged_user.userId) != kwargs['id']:
            return HttpResponseForbidden('You are not authenticated to access this page')

        return super().dispatch(request, **kwargs)

    def get_object(self):
        user = self.request.user
        return User.objects.get(userId=user.userId)

    def form_valid(self, form):
        fname = form.cleaned_data['first_name']
        lname = form.cleaned_data['last_name']
        bio = form.cleaned_data['bio']

        user = form.save(commit=False)
        if fname and lname and bio:
            user.isAuthor = True
        else:
            user.isAuthor = False

        messages.success(
            self.request, 'Profile saved successfully', extra_tags='success')
        user.save()

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        user = self.request.user
        return reverse('dashboard:editProfile', kwargs={
            'user': user.username,
            'id': user.userId
        })

@method_decorator(compress_page, name="dispatch")
class Search(View):
    template_name = 'user_profile/searchResult.html'

    def get(self, request, *args, **kwargs):
        query = request.GET['query']
        result_found = False

        if len(query) > 60 or len(query) == 0:
            search_result = []
        else:
            model = request.GET.get('model')
            if model == 'post':
                results = Post.objects.filter(title__icontains=query)
            elif model == 'draft':
                results = Draft.objects.filter(title__icontains=query)
            else:
                results = Comment.objects.filter(comment__icontains=query)

        if results:
            post_per_page = Paginator(results, 10)
            page_number = self.request.GET.get('page')
            search_result = post_per_page.get_page(page_number)
            result_found = True

        else:
            search_result = []

        context_dict = {
            'results': search_result,
            'result_length': len(search_result),
            'query': query,
            'model': model,
            'result_found': result_found
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, *args, **kwargs):
        redirect_path = request.POST.get('next')
        _id = request.POST.get('id')
        model = request.POST.get('model')

        if _id:
            if model == 'post':
                obj = Post.objects.get(postId=_id)
                obj.delete()

            if model == 'draft':
                obj = Draft.objects.get(postId=_id)
                obj.delete()

            if model == 'comment':
                action = request.POST.get('action')
                comment = Comment.objects.get(commentId=_id)

                if action == 'delete':
                    comment.delete()
                    messages.info(request, 'comment deleted')
                else:
                    approve = comment.approveOrDisapprove()
                    messages.info(
                        request, 'comment approved' if approve else 'comment Disapprove')

        return redirect(redirect_path)
