import re
import unidecode
import os

from bs4 import BeautifulSoup
from PIL import Image

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page
from django.contrib import messages
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from image_optimizer.utils import image_optimizer
from django.views.decorators.cache import never_cache

from registration.models import User
from blog.models import Tag, Post, Draft
from .forms import postForm

@requires_csrf_token
def image_upload(request):
    image_file = request.FILES['file']
    image_file = image_optimizer(
        image_data=image_file,
        output_size=(778, 519),
        resize_method='cover'
    )

    image_directory = f"uploads/{request.user}"
    image_path = os.path.join(image_directory, image_file.name)
    
    default_storage.save(image_path, image_file)
    s3_upload_url = f"https://codestim.s3.ap-south-1.amazonaws.com/{image_path}"
    file_url = default_storage.url(image_path)

    return JsonResponse({'location': f"{file_url}"}, status=201)

@method_decorator(never_cache, name="dispatch")
class CreatePost(LoginRequiredMixin, CreateView):
    '''
    This view is responsible for create a new post or
    save as draft.
    '''

    template_name = 'write_blog/writePost.html'

    def get_form_class(self):
        if 'save' in self.request.POST:
            return postForm(Draft)
        return postForm(Post)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data()
        context['writePost'] = True

        return context

    def form_valid(self, form):
        postSavingFormHandle(self.request, form)
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse(f"dashboard:{'drafts' if 'save' in self.request.POST else 'posts'}", kwargs={
            'user': user.username,
            'id': user.userId
        })

@method_decorator(never_cache, name="dispatch")
class EditOrSwitchPostToDraft(LoginRequiredMixin, View):
    '''
    This view is responsible for edit any post. Or
    Swtich back any post to draft.
    '''

    template_name = 'write_blog/writePost.html'
    form_class = postForm(Post)

    def get_object(self, obj):
        return get_object_or_404(obj, postId=self.kwargs['id'])

    def get(self, request, slug, id):
        '''
        GET request to display the post edit form with
        initial values.
        '''

        post = self.get_object(Post)
        initial = {'category': post.category, }
        form = self.form_class(initial=initial, instance=post)

        return render(request, self.template_name, {'form': form})

    def post(self, request, slug, id):
        '''
        POST request to edit post or switch back any post
        to draft.
        '''
        post = self.get_object(Post)
        form = None

        if 'update' in request.POST:

            '''
            Edit post
            '''
            form = self.form_class(request.POST or None,
                                   request.FILES, instance=post)
            if form.is_valid():
                postSavingFormHandle(self.request, form)

                return urlRedirect(request.user, 'posts')

        else:

            '''
            Switch back post to draft and remove the post
            from publish post.
            '''
            self.form_class = postForm(Draft)
            form = self.form_class(request.POST or None, request.FILES)

            if form.is_valid():
                postSavingFormHandle(self.request, form, post)
                post.delete()

                return urlRedirect(request.user, 'drafts')

        return render(request, self.template_name, {'form': form})

@method_decorator(never_cache, name="dispatch")
class EditOrPublishDraft(LoginRequiredMixin, View):
    '''
    This View is responsible for Edit draft post. Or
    Final publishing the post
    '''

    form_class = postForm(Draft)
    template_name = 'write_blog/writePost.html'

    def get_object(self):
        _id = self.kwargs['id']
        return Draft.objects.get(postId=_id)

    def get(self, request, id):
        '''
        GET request to display the draft edit form with
        initial values.
        '''

        draft = self.get_object()
        initial = {'category': draft.category, }
        form = self.form_class(initial=initial, instance=draft)

        return render(request, self.template_name, {'form': form, 'editDraft': True})

    def post(self, request, id, *args, **kwargs):
        '''
        POST request to edit drafts or finally publish as post.
        '''
        draft = self.get_object()
        form = None

        if 'update-draft' in self.request.POST:

            '''
            If user edit any draft.
            '''
            form = self.form_class(
                self.request.POST or None, request.FILES, instance=draft)

            if form.is_valid():
                postSavingFormHandle(self.request, form)
                return urlRedirect(request.user, 'drafts')
        else:

            '''
            Finally publish draft as post.
            '''
            self.form_class = postForm(Post)
            form = self.form_class(
                self.request.POST or None, request.FILES)

            if form.is_valid():
                postSavingFormHandle(self.request, form, draft)
                draft.delete()

                return urlRedirect(request.user, 'posts')

        return render(request, self.template_name, {'form': form})

def postSavingFormHandle(request, form, obj=None):
    '''
    Helper function to handle the postCreatingOrSaving form.
    # parameters
    request: http resuest object.
    form: valid form instanace.
    '''
    post = form.save(commit=False)

    author = request.user
    post.author = f"{author.first_name} {author.last_name}"
    post.authorId = f"{author.userId}"

    if 'create' in request.POST or 'switch-draft' in request.POST:
        if post.featured_image == None and obj:
            post.featured_image = obj.featured_image

    if 'create' in request.POST or 'update' in request.POST:
        new_post_body = changePostBodyImageAttributes(post.body)
        post.body = f"{new_post_body}"

        createPostMeta(post)
        createTags(post.tags, post)

    if 'create' in request.POST:
        post.publish()

    if 'update' in request.POST:
        post.update()

    if 'save' in request.POST or 'switch-draft' in request.POST:
        post.create()

    post.save()

def createTags(tags, post):
    if tags:
        tagsList = tags.split(',')
        for tag in tagsList:
            obj, created = Tag.objects.get_or_create(
                name=tag.strip().lower()
            )
        if created:
            obj.posts.add(post.title)
    else:
        Tag.objects.create(name="")


def changePostBodyImageAttributes(body):
    soup = BeautifulSoup(body, 'html.parser')
    img_tags = soup.select('img')
  
    if img_tags:
      for img in img_tags:
          if soup.select('img[src]'):
              img['data-src'] = img['src']
              del img['src']
  
          img['data-server'] = 'amazonS3'
    else:
      return body

    return soup

def urlRedirect(user, name='profile'):
    return HttpResponseRedirect(reverse(f'dashboard:{name}', kwargs={
        'user': user.username,
        'id': user.userId
    }))


def slugify(text):
    text = unidecode.unidecode(text).lower()
    slug = re.sub(r'[\W_]+', '-', text)
    if slug[:1] == '-' and slug[-1:] == '-':
        slug = slug[1:-1]
    elif slug[:1] == '-':
        slug = slug[1:]
    elif slug[-1:] == '-':
        slug = slug[:-1]

    return slug


def html2Text(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text('\n')


def createPostMeta(post):
    if post.slug == None:
        slug = slugify(post.title)
        post.slug = slug[:75]

    if post.meta_title == None:
        post.meta_title = post.title[:60]

    if post.meta_description == None:
        text = html2Text(post.body)
        post.meta_description = text[:160].strip()
