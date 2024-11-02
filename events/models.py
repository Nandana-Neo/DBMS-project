from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = CKEditor5Field(null = True,blank=True, config_name='extends')
    date = models.DateField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('event-detail' , kwargs={'pk' : self.pk})
    
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_events')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)  # New field for attendance

    class Meta:
        unique_together = ('event', 'user')  # Each user can only participate once

    def __str__(self):
        return f"{self.user.username} in {self.event.name}"

# class Attendance(models.Model):
#     participant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE, related_name="attendance")
#     date = models.DateField()

#     def __str__(self):
#         return f"Attendance for {self.participant.user.username} on {self.date}"
