from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '您的姓名'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '您的邮箱（不会公开）'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '您的网站（可选）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '写下您的评论...'
            }),
        }
        labels = {
            'name': '姓名',
            'email': '邮箱',
            'website': '网站',
            'content': '评论内容',
        }


class SearchForm(forms.Form):
    """搜索表单"""
    q = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '搜索文章...',
        }),
        label=''
    )
