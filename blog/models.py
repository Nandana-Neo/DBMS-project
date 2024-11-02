from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field(null = True,blank=True, config_name='extends')
    # content = RichTextField(blank=True,null=True)
    # content = models.TextField()
    #date_posted = models.DateTimeField(auto_now_add=True) #only when object is created -- but can't edit the field
    date_posted=models.DateTimeField(default=timezone.now) # not putting now() because we need the actual function as default value
    author = models.ForeignKey(User,on_delete=models.CASCADE) #delete post when user is deleted
    likes= models.ManyToManyField(User,blank=True,null=True,related_name='liked_posts')
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail' , kwargs={'pk' : self.pk})