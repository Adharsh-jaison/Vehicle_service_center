from django.db import models
from django.contrib.auth.models import User
from owner.models import ServiceProfile


class user_details(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    # Phone=models.BigIntegerField(null=True)
    # Qualification=models.CharField(max_length=100,null=False)
    Interest=models.CharField(max_length=100,null=False)
    # CurrentStatus=models.CharField(max_length=100,null=True)
    # Institution=models.CharField(max_length=100,null=False)
   

# class feedback(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE,default=0)
#     name=models.CharField(max_length=100,null=True)
#     Date=models.DateField(null=False)
#     Instructor=models.CharField(max_length=100,null=False)
#     Content=models.IntegerField(null=False)
#     levelofteaching=models.IntegerField(null=False)
#     Material=models.IntegerField(null=False)
#     Rating=models.IntegerField(null=False)
#     Overallrating=models.IntegerField(null=False)
#     Comments=models.CharField(max_length=100,null=False) 
    
class interests(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=0)
    Subject=models.CharField(max_length=100,null=False)
    Teaching_status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Subject.__str__())
    
class improvements(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=0)
    Subject=models.CharField(max_length=100,null=False)
    Learning=models.CharField(max_length=100,null=False)

    def __str__(self):
        return str(self.Subject.__str__())
    
class teching(models.Model):
    teach_by=models.ForeignKey(User,related_name='teachingBy',on_delete=models.CASCADE, default=0)
    teach_to=models.ForeignKey(User,related_name='teachingTo',on_delete=models.CASCADE, default=0)
    sub = models.CharField(null=False,max_length=225,default=0)
    teach_status=models.IntegerField(default=0)



class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=0)  
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    full_name=models.CharField(max_length=20, null=True, blank=True)
    user_image = models.ImageField(upload_to='uploads/',null=True,blank=True)
    # def __str__(self):
    #     return self.user.username
    def __str__(self):
        return f'{self.user.username} Profile'





class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Billing..', 'Billing..'),
        ('Completed', 'Completed'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service_center = models.ForeignKey(ServiceProfile, on_delete=models.CASCADE)
    service_date = models.DateField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=50,blank=True, null=True)
    mechanic_on_site = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')],blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    vehicle_model = models.CharField(max_length=100,blank=True, null=True)
    vehicle_number = models.CharField(max_length=20,blank=True, null=True)
    vehicle_location = models.CharField(max_length=255,blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)  # Whether the bill has been paid
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.customer.username} for {self.service_center.service_center_name} on {self.service_date}"



class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer or service center
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')  # Link to booking
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_service_center = models.BooleanField(default=False)  # True if the message is from the service center

    def __str__(self):
        return f"Booking {self.booking.id} - {self.sender.username} - {self.message[:20]}"
    


class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,default=1)  # Linking feedback to a booking
    date = models.DateField(null=True, blank=True)
    
    # How would you rate the quality of the service you received? (1-5 scale)
    service_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Were the staff at the service center helpful and professional? (Descriptive choices)
    staff_professionalism = models.CharField(max_length=50, choices=[
        ('Very Unprofessional', 'Very Unprofessional'),
        ('Unprofessional', 'Unprofessional'),
        ('Neutral', 'Neutral'),
        ('Professional', 'Professional'),
        ('Very Professional', 'Very Professional')
    ], null=True, blank=True)
    
    # Did the service center meet your expectations? (1-4 scale)
    expectations_met = models.CharField(max_length=50,choices=[
        ('Did Not Meet Expectations', 'Did Not Meet Expectations'),
        ('Below Expectations', 'Below Expectations'),
        ('Met Expectations', 'Met Expectations'),
        ('Exceeded Expectations', 'Exceeded Expectations')
    ], null=True, blank=True)
    
    # Was your service completed within the expected time frame? (1-4 scale)
    completion_timeframe = models.CharField(max_length=50,choices=[
        ('Far Exceeded Timeframe', 'Far Exceeded Timeframe'),
        ('Exceeded Timeframe', 'Exceeded Timeframe'),
        ('Met Timeframe', 'Met Timeframe'),
        ('Under Timeframe', 'Under Timeframe')
    ], null=True, blank=True)

    # Suggestions text field
    suggestions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Feedback for {self.booking.service_center.name}' 