from django import forms
from .models import Event, EventParticipant

class EventForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Event
        fields = ['name', 'description', 'date']
        

class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = []
