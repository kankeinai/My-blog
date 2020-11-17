from django import forms
from .models import Post, Comment, Topic


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'topic', 'details', 'text')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)
