# blog/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.db.models import F


class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True, default="python")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,)
    details = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def prev_post(self):
        posts = Post.objects.filter(
            topic=self.topic, published_date__isnull=False).order_by('-published_date')
        for post in posts:
            if post.published_date < self.published_date:
                return post.pk
        return self.pk

    def next_post(self):
        posts = Post.objects.filter(
            topic=self.topic, published_date__isnull=False).order_by('published_date')
        for post in posts:
            if post.published_date > self.published_date:
                return post.pk
        return self.pk

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_views(self):
        Post.objects.filter(pk=self.pk).update(views=F('views') + 1)
        return self.views

    def get_related_posts(self):
        posts = Post.objects.filter(
            topic=self.topic, published_date__isnull=False).order_by('published_date')
        return posts

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
