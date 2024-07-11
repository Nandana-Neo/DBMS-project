from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView
                                  )
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import Post
from django.http import JsonResponse
from django.utils.dateparse import parse_date



# Create your views here.


# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')

### NOT USED NOW--- class based view is used
def home(request):
    context={
        'posts' : Post.objects.all()
    }
    return render(request,'blog/home.html',context) #use context in  the template

class PostListView(ListView):
    model = Post #Which model to query to get list
    template_name='blog/home.html'   # <app> / <model>_<viewtype>.html
    context_object_name = 'posts' # object_name was by default object_list
    ordering = ['-date_posted'] #default oldest -> newest
    paginate_by = 5

class UserPostListView(ListView):
    model = Post #Which model to query to get list
    template_name='blog/user_posts.html'   # <app> / <model>_<viewtype>.html
    context_object_name = 'posts' # object_name was by default object_list
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404( User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=get_object_or_404( User, username = self.kwargs.get('username'))
        context['profile_user'] = user
        context['is_owner'] = self.request.user == user
        return context
    

class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked=False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['already_liked']=liked
        return context

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post= self.get_object() 
        if(self.request.user == post.author):
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form): # overriding the default form method
        form.instance.author = self.request.user
        return super().form_valid(form) # default method

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form): # overriding the default form method
        form.instance.author = self.request.user
        return super().form_valid(form) # default method = >saving
    
    def test_func(self):
        post= self.get_object() # gets the post we r trying to edit
        if(self.request.user == post.author):
            return True
        return False
     


def about(request):
    return render(request,'blog/about.html',{'title' : 'About'})

@login_required
def LikeView(request, pk):
    post=get_object_or_404(Post, id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        likes=True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


    

def blogpost_list(request):
    posts = Post.objects.all()
    events = []
    for post in posts:
        events.append({
            'title': '',
            'start': post.date_posted.strftime('%Y-%m-%d'),
            'display': 'background'  # This makes the dot visible without a title
        })
    return JsonResponse(events, safe=False)

class get_posts_by_dateListView(ListView):
    model = Post #Which model to query to get list
    template_name='blog/posts_by_date.html'   # <app> / <model>_<viewtype>.html
    context_object_name = 'posts' # object_name was by default object_list
    paginate_by = 5

    def get_queryset(self,**kwargs):
        date= self.kwargs.get('date')
        return Post.objects.filter(date_posted__date=date)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.kwargs.get('date')
        return context
    