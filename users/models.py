from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_ckeditor_5.fields import CKEditor5Field

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image= models.ImageField(default='default.jpg', upload_to='profile_pics')
    # about= models.TextField(default='Hi There')
    # about= RichTextField(default='Hi There')
    about= CKEditor5Field(null = True,default= 'Hi There', config_name='extends')
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self,*args,**kwargs):# already exiting method to save -- we are overriding it

        # Delete the old image file if it exists and is not the default image
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image.name != 'default.jpg':
                this.image.delete(save=False)
        except Profile.DoesNotExist:
            pass

        super(Profile,self).save(*args, **kwargs)  #The original parent classes' save method happens - one that was defaultly happening
        img = Image.open(self.image.path)
        if (img.height > 300 or img.width > 300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)