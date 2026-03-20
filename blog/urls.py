from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('page/<slug:slug>/', views.StaticPageView.as_view(), name='static_page'),
    path('links/', views.LinkListView.as_view(), name='links'),
    path('guestbook/', views.GuestbookCreateView.as_view(), name='guestbook'),
]
