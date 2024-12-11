from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class ServiceProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=0)
    location=models.CharField(max_length=255,null=True,blank=True)
    vehicle_make=models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    service_center_name = models.CharField(max_length=255,null=True,blank=True)
    operating_hours = models.CharField(max_length=100,null=True,blank=True)
    available_services = models.TextField(null=True,blank=True)
    pricing = models.TextField(null=True,blank=True)
    ratings_reviews = models.TextField(null=True,blank=True)
    service_center_type = models.CharField(max_length=100,null=True,blank=True)
    facilities = models.TextField(null=True,blank=True)
    manager_name = models.CharField(max_length=100,null=True,blank=True)
    booking_availability = models.IntegerField(null=True,blank=True)
    payment_methods = models.CharField(max_length=255,null=True,blank=True)
    service_center_image = models.ImageField(upload_to='uploads/',null=True,blank=True)
    # service_center_image = models.ImageField(upload_to='service_center_images/', blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    

