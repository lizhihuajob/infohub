from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView, View
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
import markdown
from .models import Post, Category, Tag, Comment, Link, Page, Guestbook
from .forms import CommentForm, GuestbookForm


class BaseMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 热门文章 - 按阅读量
        context['hot_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        # 分类目录树
        context['categories'] = Category.objects.all()
        # 标签云 - 按文章数量排序
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')
        # 最新评论
        context['recent_comments'] = Comment.objects.filter(status='approved').order_by('-created_at')[:5]
        return context


class HomeView(BaseMixin, ListView):
    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')


class PostDetailView(BaseMixin, DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        # 增加阅读量
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # 渲染Markdown内容
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'tables'])
        context['content_html'] = md.convert(post.content)
        context['toc'] = md.toc
        
        # 已通过审核的评论
        context['comments'] = Comment.objects.filter(post=post, status='approved', parent=None)
        
        # 评论表单
        context['comment_form'] = CommentForm()
        
        # 上一篇/下一篇
        try:
            context['previous_post'] = Post.objects.filter(
                status='published',
                publish_date__lt=post.publish_date
            ).order_by('-publish_date').first()
        except Post.DoesNotExist:
            context['previous_post'] = None
            
        try:
            context['next_post'] = Post.objects.filter(
                status='published',
                publish_date__gt=post.publish_date
            ).order_by('publish_date').first()
        except Post.DoesNotExist:
            context['next_post'] = None
            
        return context


class CategoryDetailView(BaseMixin, ListView):
    template_name = 'blogapp/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category
        ).select_related('author').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagDetailView(BaseMixin, ListView):
    template_name = 'blogapp/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            tags=self.tag
        ).select_related('category', 'author').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchView(BaseMixin, ListView):
    template_name = 'blogapp/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return Post.objects.filter(
                Q(status='published') &
                (Q(title__icontains=self.query) | Q(content__icontains=self.query))
            ).select_related('category', 'author').prefetch_related('tags')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context


class PageDetailView(BaseMixin, DetailView):
    model = Page
    template_name = 'blogapp/page_detail.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        context['content_html'] = md.convert(page.content)
        return context


class AboutView(BaseMixin, DetailView):
    template_name = 'blogapp/page_detail.html'
    context_object_name = 'page'

    def get_object(self):
        return get_object_or_404(Page, page_type='about')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        context['content_html'] = md.convert(page.content)
        return context


class LinksView(BaseMixin, ListView):
    template_name = 'blogapp/links.html'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page = Page.objects.get(page_type='links')
            md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
            context['page_content'] = md.convert(page.content)
            context['page_title'] = page.title
        except Page.DoesNotExist:
            context['page_content'] = ''
            context['page_title'] = '友情链接'
        return context


class GuestbookView(BaseMixin, FormView):
    template_name = 'blogapp/guestbook.html'
    form_class = GuestbookForm
    success_url = reverse_lazy('blogapp:guestbook')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Guestbook.objects.filter(status='approved').order_by('-created_at')
        try:
            page = Page.objects.get(page_type='guestbook')
            md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
            context['page_content'] = md.convert(page.content)
            context['page_title'] = page.title
        except Page.DoesNotExist:
            context['page_content'] = ''
            context['page_title'] = '留言板'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '留言已提交，审核通过后将显示。')
        return super().form_valid(form)


class CommentCreateView(FormView):
    form_class = CommentForm

    def post(self, request, post_id, *args, **kwargs):
        self.post = get_object_or_404(Post, id=post_id, status='published')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.post
        comment.save()
        messages.success(self.request, '评论已提交，审核通过后将显示。')
        return redirect(self.post.get_absolute_url() + '#comments')

    def form_invalid(self, form):
        messages.error(self.request, '评论提交失败，请检查表单。')
        return redirect(self.post.get_absolute_url() + '#comments')
