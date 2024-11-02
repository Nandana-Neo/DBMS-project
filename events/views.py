from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView
                                  )
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .models import Event, EventParticipant
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

# Create your views here.
class EventListView(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20
    ordering = ['date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events"
        context['title'] = title
        context['cal'] = "events"
        return context

class EventUserListView(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
    # Filter events by the "organized_events" related field for the logged-in user
        return self.model.objects.filter(organizer=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events Organized"
        context['title'] = title
        context['cal'] = "events"
        return context
    
class EventRegListView(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.filter(participants__user=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Events Registered"
        context['title'] = title
        context['cal'] = "events"
        return context

class EventDetailView(LoginRequiredMixin,DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reg = False
        if self.request.user.is_authenticated:
            if self.object.participants.filter(user=self.request.user).exists():
                reg = True
        context['reg'] = reg
        context['cal'] = "events"
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'description','date']
    def form_valid(self, form): # overriding the default form method
        form.instance.organizer = self.request.user
        return super().form_valid(form) # default method
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cal'] = "events"
        return context

class EventDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/events/'

    def test_func(self):
        post= self.get_object() 
        if(self.request.user == post.organizer):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cal'] = "events"
        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cal'] = "events"
        return context

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
        context['cal'] = "events"
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
    
@login_required
def event_search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')  # Type filter for 'user' or 'event'
    
    users = []
    events = []
    
    if search_type == 'user' or search_type == 'all':
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query))
    
    if search_type == 'event' or search_type == 'all':
        events = Event.objects.filter(name__icontains=query)

    return render(request, 'search/event_search_results.html', {'title': "Events" ,'users': users, 'events': events, 'query': query, 'search_type': search_type, 'cal': "events"})

@login_required
def UserEventView(request, username):
    user = get_object_or_404(User, username=username)
    
    # Events organized by the user
    organized_events = Event.objects.filter(organizer=user).order_by('-date')
    organized_count = organized_events.count()
    
    # Events the user has registered for
    registered_events = EventParticipant.objects.filter(user=user).values_list('event', flat=True)
    registered_events = Event.objects.filter(id__in=registered_events).order_by('-date')
    registered_count = registered_events.count()

    # Paginate organized events
    paginator_organized = Paginator(organized_events, 6)
    page_number_organized = request.GET.get('orgpg')
    try:
        organized_events = paginator_organized.page(page_number_organized)
    except PageNotAnInteger:
        organized_events = paginator_organized.page(1)
    except EmptyPage:
        organized_events = paginator_organized.page(paginator_organized.num_pages)

    # Paginate registered events
    paginator_registered = Paginator(registered_events, 6)
    page_number_registered = request.GET.get('regpg')
    try:
        registered_events = paginator_registered.page(page_number_registered)
    except PageNotAnInteger:
        registered_events = paginator_registered.page(1)
    except EmptyPage:
        registered_events = paginator_registered.page(paginator_registered.num_pages)

    is_owner = (request.user == user)
    
    context = {
        'profile_user': user,
        'is_owner': is_owner,
        'organized_events': organized_events,
        'registered_events': registered_events,
        'total_organized': organized_count,
        'total_registered': registered_count,
        'title': f"Events by {user.first_name}",
        'cal': "events"
    }
    return render(request, 'events/user_events.html', context)

def event_date_list(request):
    posts = Event.objects.all()
    events = []
    for post in posts:
        events.append({
            'title': '',
            'start': post.date.strftime('%Y-%m-%d'),
            'display': 'background'  # This makes the dot visible without a title
        })
    return JsonResponse(events, safe=False)

class get_events_by_date(LoginRequiredMixin,ListView):
    model = Event #Which model to query to get list
    template_name='events/events_by_date.html'   # <app> / <model>_<viewtype>.html
    context_object_name = 'posts' # object_name was by default object_list
    paginate_by = 5

    def get_queryset(self,**kwargs):
        date= self.kwargs.get('date')
        return Event.objects.filter(date=date)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.kwargs.get('date')
        context['cal'] = "events"
        return context