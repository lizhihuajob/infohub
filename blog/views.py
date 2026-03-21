from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from taggit.models import Tag
from .models import Post, Category, Link, StaticPage
from comments.models import Comment, GuestbookMessage


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('category', 'author')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(status='approved', parent=None).prefetch_related('replies')
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['next_post'] = self.object.get_next_post()
        context['previous_post'] = self.object.get_previous_post()
        return context


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', category=self.category).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', tags__slug=self.tag.slug).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class SearchView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                status='published'
            ).filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class StaticPageView(DetailView):
    model = StaticPage
    template_name = 'blog/static_page.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return get_object_or_404(StaticPage, slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        if self.object.page_type == 'guestbook':
            context['guestbook_messages'] = GuestbookMessage.objects.filter(status='approved')
        return context


class LinkListView(ListView):
    model = Link
    template_name = 'blog/links.html'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class CommentCreateView(CreateView):
    model = Comment
    fields = ['author_name', 'author_email', 'author_url', 'content', 'parent']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        form.instance.post = post
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')
        form.instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        messages.success(self.request, '评论已提交，等待审核后显示。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.kwargs['slug']})


class GuestbookCreateView(CreateView):
    model = GuestbookMessage
    fields = ['author_name', 'author_email', 'content']
    template_name = 'blog/guestbook_form.html'
    success_url = reverse_lazy('blog:guestbook')

    def form_valid(self, form):
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')
        messages.success(self.request, '留言已提交，等待审核后显示。')
        return super().form_valid(form)
