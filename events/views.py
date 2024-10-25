from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView
                                  )
from .models import Event, EventParticipant
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 5

class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reg = False
        if self.object.participants.filter(user=self.request.user).exists():
            reg = True
        context['reg'] = reg
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'description','date']
    def form_valid(self, form): # overriding the default form method
        form.instance.organizer = self.request.user
        return super().form_valid(form) # default method

class EventDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/events/'

    def test_func(self):
        post= self.get_object() 
        if(self.request.user == post.organizer):
            return True
        return False


class EventUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['name', 'description','date']

    def form_valid(self, form): # overriding the default form method
        form.instance.organizer = self.request.user
        return super().form_valid(form) # default method = >saving
    
    def test_func(self):
        post= self.get_object() # gets the post we r trying to edit
        if(self.request.user == post.organizer):
            return True
        return False

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Check if the user is not the organizer and isn't already registered
    if request.user != event.organizer:
        EventParticipant.objects.get_or_create(event=event, user=request.user)
    else:
        return HttpResponseForbidden("You cannot register for your own event.")
    
    return redirect('event-detail', pk=event.pk)    

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Event
#     fields = ['name', 'content']
#     def form_valid(self, form): # overriding the default form method
#         form.instance.author = self.request.user
#         return super().form_valid(form) # default method
