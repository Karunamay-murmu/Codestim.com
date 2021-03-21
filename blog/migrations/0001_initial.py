# Generated by Django 3.0.7 on 2020-12-31 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import image_optimizer.fields
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField()),
                ('message_type', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(default=None, max_length=255, unique=True)),
                ('postId', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('authorId', models.CharField(default=None, editable=False, max_length=255)),
                ('tags', models.CharField(default=None, max_length=255)),
                ('body', tinymce.models.HTMLField()),
                ('featured_image', image_optimizer.fields.OptimizedImageField(blank=True, null=True, upload_to='featured_image')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True)),
                ('slug', models.SlugField(blank=True, max_length=75, null=True, unique=True)),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True)),
                ('author', models.CharField(max_length=256)),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('update_date', models.DateField(blank=True, null=True)),
                ('read_time', models.CharField(default='3 min', max_length=10)),
                ('liked', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Categorie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subscriber_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('posts', models.ManyToManyField(to='blog.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('title', models.CharField(default=None, max_length=255, unique=True)),
                ('postId', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('authorId', models.CharField(default=None, editable=False, max_length=255)),
                ('tags', models.CharField(default=None, max_length=255)),
                ('body', tinymce.models.HTMLField()),
                ('featured_image', image_optimizer.fields.OptimizedImageField(blank=True, null=True, upload_to='featured_image')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True)),
                ('slug', models.SlugField(blank=True, max_length=75, null=True, unique=True)),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True)),
                ('create_date', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Categorie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('isApprove', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
