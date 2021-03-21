import uuid
from io import BytesIO
from PIL import Image

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files import File

from image_optimizer.fields import OptimizedImageField

from tinymce.models import HTMLField
from registration.models import User


class Categorie(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class PostInfo(models.Model):
    title = models.CharField(max_length=255, unique=True, default=None)
    postId = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    authorId = models.CharField(max_length=255, default=None, editable=False)
    category = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, default=None)
    tags = models.CharField(max_length=255, default=None)
    body = HTMLField()
    featured_image = OptimizedImageField(
        upload_to="featured_image",
        optimized_image_output_size=(772, 440),
        optimized_image_resize_method='cover',
        blank=True,
        null=True
    )
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    slug = models.SlugField(max_length=75, unique=True, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        abstract = True


class Post(PostInfo):
    author = models.CharField(max_length=256)
    publish_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    read_time = models.CharField(max_length=10, default="3 min")
    liked = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def update(self):
        self.update_date = timezone.now()
        self.save()

    def totalLikes(self):
        return self.liked


class Draft(PostInfo):
    create_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def create(self):
        self.create_date = timezone.now()
        self.save()


class Tag(models.Model):
    tagId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name


class Comment(models.Model):
    commentId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    create_date = models.DateField(default=timezone.now)
    isApprove = models.BooleanField(default=False)

    def approveOrDisapprove(self):
        self.isApprove = False if self.isApprove else True
        self.save()

        return self.isApprove

    def __str__(self):
        return self.comment


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    message_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"({self.message_type}){self.message}"

    def get_absolute_url(self):
        return reverse('blog:contact')


class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)
    subscriber_email = models.EmailField(unique=True)

    def __str__(self):
        return self.subscriber_email
