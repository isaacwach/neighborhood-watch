from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_pics')
    status = models.TextField(max_length=100)
    national_id = models.CharField(max_length=20,default=1)
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        super().save()

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
    
    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile
    
    def delete_profile(self):
        self.delete()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()