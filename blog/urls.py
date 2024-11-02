from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    # UserPostListView,
                    LikeView,
                    blogpost_list,
                    get_posts_by_date,
                    UserPostView
                    )
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',PostListView.as_view(), name='blog-home'),
    path('user/<str:username>',UserPostView, name='user-posts'),
    path('about/',views.about,name='blog-about'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('like/<int:pk>',LikeView,name='like_post'),

    # path('events/',TemplateView.as_view(template_name='blog/events.html'),name='events'),

    path('blogs/calendar/<str:date>/', get_posts_by_date.as_view(), name='get_posts_by_date'),
    path('blogs/api/posts/',blogpost_list,name='blogpost-list'),
    path('search/blog/', views.blog_search, name='blog_search'),
]
