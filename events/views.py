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
    paginate_by = 20
    ordering = ['date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events"
        context['title'] = title
        return context

class EventUserListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20
    ordering = ['date']

    def get_queryset(self):
    # Filter events by the "organized_events" related field for the logged-in user
        return self.model.objects.filter(organizer=self.request.user).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events Organized"
        context['title'] = title
        return context
    
class EventRegListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20
    ordering = ['date']

    def get_queryset(self):
        return Event.objects.filter(participants__user=self.request.user).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events Registered"
        context['title'] = title
        return context

class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reg = False
        if self.request.user.is_authenticated:
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

class MarkAttendanceView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = EventParticipant
    template_name = 'events/mark_attendance.html'
    context_object_name = 'participants'

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return EventParticipant.objects.filter(event=event)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['pk'])  # Add the event to context
        return context
    
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        participants = self.get_queryset()

        # Update attendance for each participant
        for participant in participants:
            attended = request.POST.get(f'attended_{participant.id}', 'off') == 'on'
            participant.attended = attended
            participant.save()

        return redirect('event-detail', pk=event.pk)

    # Ensure only organizer can access
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return self.request.user == event.organizer