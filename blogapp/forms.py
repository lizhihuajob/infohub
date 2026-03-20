from django import forms
from .models import Comment, Guestbook


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'author_url', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '您的昵称',
                'required': 'required'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '您的邮箱（不会公开）',
                'required': 'required'
            }),
            'author_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '您的网站（可选）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '写下您的评论...',
                'required': 'required'
            }),
        }
        labels = {
            'author_name': '昵称',
            'author_email': '邮箱',
            'author_url': '网站',
            'content': '内容',
        }


class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['author_name', 'author_email', 'author_url', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '您的昵称',
                'required': 'required'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '您的邮箱（不会公开）',
                'required': 'required'
            }),
            'author_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '您的网站（可选）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '写下您的留言...',
                'required': 'required'
            }),
        }
        labels = {
            'author_name': '昵称',
            'author_email': '邮箱',
            'author_url': '网站',
            'content': '内容',
        }
