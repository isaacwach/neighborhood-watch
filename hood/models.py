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

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hood')
    hood_photo = models.ImageField(upload_to='hoods/')
    description = models.TextField()
    health_number = models.IntegerField(null=True, blank=True)
    police_number = models.IntegerField(null=True, blank=True)
    occupant_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}hood'

    def save_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()
        
    @classmethod
    def find_neighbourhood(cls, neighbourhood_id):
        return cls.objects.filter(id=neighbourhood_id)
    
    @classmethod
    def update_occupants(cls,neighbourhood_id):
        occupation = cls.objects.get(id=neighbourhood_id)
        new_count = occupation.occupation_count + 1
        cls.objects.filter(id = neighbourhood_id).update(occupation_count = new_count)

    def update_neighborhood(self):
        name = self.name
        self.name = name