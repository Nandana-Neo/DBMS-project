from django.db.models.signals import post_save # signal
from django.contrib.auth.models import User # sender
from django.dispatch import receiver # reciever decorator

from .models import Profile

# When a user is saved, send signal 'post_save'
# This signal is received by the receiver and goes into the function
# create_profile fn-receiver- takes all arguments post_save signal passes into it

@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) #If a user is created then create a profile object with user=instance of the user that was created

@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):
    instance.profile.save()
        