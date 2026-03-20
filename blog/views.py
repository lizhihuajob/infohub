from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from .models import Post, Category, Tag, Page, Comment
from .forms import CommentForm, SearchForm


class CustomLoginView(LoginView):
    """自定义登录视图"""
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context

    def form_invalid(self, form):
        messages.error(self.request, '用户名或密码错误，请重试。')
        return super().form_invalid(form)


class HomeView(ListView):
    """首页 - 文章列表"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class PostDetailView(DetailView):
    """文章详情页"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 增加阅读量
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # 上一篇/下一篇
        context['prev_post'] = Post.objects.filter(
            status='published',
            published_at__lt=post.published_at
        ).order_by('-published_at').first()
        
        context['next_post'] = Post.objects.filter(
            status='published',
            published_at__gt=post.published_at
        ).order_by('published_at').first()
        
        # 评论列表（只显示已通过审核的）
        context['comments'] = post.comments.filter(
            status='approved',
            parent=None
        ).order_by('-created_at')
        
        # 评论表单
        context['comment_form'] = CommentForm()
        
        return context


class CategoryView(ListView):
    """分类文章列表"""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category
        ).select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagView(ListView):
    """标签文章列表"""
    model = Post
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            tags=self.tag
        ).select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchView(ListView):
    """搜索页面"""
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
            ).select_related('author', 'category').prefetch_related('tags')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_form'] = SearchForm(initial={'q': context['query']})
        return context


class PageView(DetailView):
    """静态页面"""
    model = Page
    template_name = 'blog/page.html'
    context_object_name = 'page'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)


class CommentView(View):
    """处理评论提交"""
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='published')
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            
            # 检查是否为回复
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent = Comment.objects.get(id=parent_id, post=post)
                    comment.parent = parent
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
            messages.success(request, '评论已提交，等待审核后显示。')
        else:
            messages.error(request, '评论提交失败，请检查表单。')
        
        return redirect(post.get_absolute_url())
