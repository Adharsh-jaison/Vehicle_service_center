from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .models import user_details, interests, improvements,teching
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from owner.views import dashboard
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from owner.models import ServiceProfile
# from owner.views import pay_bill
from .models import Booking
from .models import Feedback
# Create your views here.






def user_profile(request):
        
        if UserProfile.objects.filter(user=request.user).exists():
          user_profile = UserProfile.objects.get(user=request.user)
        else:
          user_profile = ServiceProfile(user=request.user)

        if request.method == 'POST':
            # Update address
            if request.POST['address']:
                user_profile.address = request.POST['address']

            # Update phone number
            if  request.POST['phone']:
                user_profile.phone = request.POST['phone']

            if  request.POST['full_name']:
                user_profile.full_name = request.POST['full_name']
            
            if request.FILES.get('user_image'):
                print(request.FILES['user_image'])
                user_profile.user_image = request.FILES['user_image']
                print("halo")
            user_profile.save()
            return redirect('userprofile')  # Redirect after saving

        # Render the user's profile details
        booking = Booking.objects.filter(customer=request.user)

        return render(request, "user/main/userprofile.html", {
            'user_profil': user_profile,
            'booking':booking,
        })
        # return render(request,"user/main/userprofile.html",{'booking': booking})



def index(request):
    return render(request,"user/main/index.html")

def about(request):
    return render(request,"user/main/about.html")
def courses(request):
    return render(request,"user/main/courses.html")

def bill_success(request):
    booking = Booking.objects.filter(customer=request.user)
    return render(request,"user/main/bill_success.html")


def pay_bill(request,booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Payment processing logic here (e.g., integrate payment gateway)
        booking.paid = True  # Mark the booking as paid
        booking.status = 'completed'  # Update the status to completed
        booking.save()

        return render(request,'user/main/bill_success.html',{'booking': booking})

    return render(request,'user/main/feedback_form.html', {'booking': booking})



def user_book(request, service_provider_id):
    service_provider = get_object_or_404(ServiceProfile, id=service_provider_id)
  
    if request.method == 'POST':
        # Extract data from the request
        service_date = request.POST.get('service_date')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_number = request.POST.get('vehicle_number')
        mechanic_on_site = request.POST.get('mechanic_on_site')
        vehicle_location = request.POST.get('vehicle_location')
        additional_info = request.POST.get('additional_info')

        # Create a new booking and associate it with the service provider
        booking = Booking.objects.create(
            customer=User.objects.get(id=request.user.id),
            service_center=service_provider,  # Associate with the service provider
            service_date=service_date,
            vehicle_type=vehicle_type,
            vehicle_model=vehicle_model,
            vehicle_number=vehicle_number, 
            mechanic_on_site=mechanic_on_site,
            vehicle_location=vehicle_location,
            additional_info=additional_info,
            status='Pending'  # Set initial status
        )
        booking.save()
        print("Booking created successfully.")
        # return render(request,'userprofile',{'success': True, 'booking_id': booking.id})
        return redirect('userprofile')

    return render(request,'user/main/user_book.html', {'service_provider': service_provider})
    




def feedback_form(request, booking_id):
    # Get the booking object based on the booking ID
    booking = get_object_or_404(Booking, id=booking_id)
  # Assuming the booking has a related service center

    if request.method == 'POST':
        # Get form data from POST request
        date = request.POST['date']
        service_quality = request.POST['service_quality']
        staff_professionalism = request.POST['staff_professionalism']
        expectations_met = request.POST['expectations_met']
        completion_timeframe = request.POST['completion_timeframe']
        msg = request.POST['suggestions']  # Suggestions

        # Create and save the feedback object
        feedback = Feedback.objects.create(
            date=date,
            service_quality=service_quality,
            staff_professionalism=staff_professionalism,
            expectations_met=expectations_met,
            completion_timeframe=completion_timeframe,
            suggestions=msg,  # Store suggestions
            booking=booking,  # Associate feedback with the booking

        )
        feedback.save()

        return redirect('userprofile')  # Redirect to a success page or another view

    return render(request,'user/main/feedback_form.html')

# def feedback_view(request,booking_id): 
#     feedback_list = Feedback.objects.all(Feedback,id=booking_id)

#     return render(request, 'owner/main/feedback_view.html', {
#         'feedback_list': feedback_list,'booking_id':booking_id
#     })

def feedback_view(request):
    # Get the current user (assuming they have staff status)
    # current_user = request.user
    
    # Get the bookings for the current service center user
    bookings = Booking.objects.filter(service_center=ServiceProfile.objects.get(user=request.user.id))

    # Get feedback for the current user's bookings
    feedback_list = Feedback.objects.filter(booking__in=bookings)

    return render(request, 'owner/main/feedback_view.html', {
        'feedback_list': feedback_list,  # Pass feedback to the template
        'bookings': bookings,              # Optionally pass bookings to the template
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            if user.is_superuser==False and user.is_staff==True:
                login(request,user)
                return redirect('home')
            elif user.is_superuser==False and user.is_staff==False:
                login(request,user)
                return redirect('userprofile')
        elif user is None:
            msg = "Wrong credentials. Please try again!"
            return render(request , 'user/main/login.html' , {'msg':msg})
    return render(request , 'user/main/login.html')





def user_register(request):
    if request.method=='POST':
        username=request.POST['name']
        if User.objects.filter(username=username).exists():
            msg = 'username already exists!'
            return render(request, 'user/main/register.html',{'msg':msg})
        else:
            email=request.POST['email']
            password=request.POST['password']
            # phone=request.POST['phone']
            # qualification=request.POST['qualification']
            # current=request.POST['current']
            # institution=request.POST['institution']
            interest=request.POST['interest']
            new_password = make_password(password)
            if interest=='Workshop Owner':
                a=True
                User.objects.create(username=username,email=email,password=new_password,is_staff=a)
                return redirect('success')
            else:
                a=False
                User.objects.create(username=username,email=email,password=new_password,is_staff=a)
                return redirect('success')
        
            
    return render(request, 'user/main/register.html')




def success(request):
    return render(request,'user/main/success.html')

def user_logout(request):
    logout(request)
    return redirect('Login')

def search_service(request):
    items = ServiceProfile.objects.all()  # Retrieve all items
    return render(request, 'user/main/search_service.html', {'items': items})
   


    
def thanks(request):
    return render(request,'user/main/thanks.html')




from .models import UserProfile

def user_edit(request):
    if request.method == 'POST':
        
        # Check if 'address' is present in the POST request and update it
        if 'address' in request.POST and request.POST['address']:
            address = request.POST['address']
            user_profil, created = UserProfile.objects.get_or_create(user=request.user)
            user_profil.address = address
            user_profil.save()

        # Check if 'phone' is present in the POST request and update it
        if 'phone' in request.POST and request.POST['phone']:
            phone = request.POST['phone']
            user_profil, created = UserProfile.objects.get_or_create(user=request.user)
            user_profil.phone = phone
            user_profil.save()
        
        if 'full_name' in request.POST and request.POST['full_name']:
            full_name = request.POST['full_name']
            user_profil, created = UserProfile.objects.get_or_create(user=request.user)
            user_profil.full_name = full_name
            user_profil.save()
        
        if request.FILES.get('user_image'):
                
                if UserProfile.objects.filter(user=request.user).exists():
                  user_profile = UserProfile.objects.get(user=request.user)
                else:
                   user_profile = ServiceProfile(user=request.user)
                   print(request.FILES['user_image'])
                   user_profile.user_image = request.FILES['user_image']
                   print("halo")
                user_profile.save()
                print("notsaved")

        return redirect('userprofile')  # Redirect back to the user's profile page after saving

    # Render the edit page if request method is GET
    return render(request, "user/main/edit.html")









from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def book_service(request,service_provider_id):
    service_provider = get_object_or_404(ServiceProfile, id=service_provider_id)
    if request.method == 'POST':
        # Extract data from the request
        service_date = request.POST.get('service_date')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_number = request.POST.get('vehicle_number')
        mechanic_on_site = request.POST.get('mechanic_on_site')
        vehicle_location = request.POST.get('vehicle_location')
        additional_info = request.POST.get('additional_info')

        # Create a new booking
        booking = Booking.objects.create(
            customer=request.user,
            service_date=service_date,
            vehicle_type=vehicle_type,
            vehicle_model=vehicle_model,
            vehicle_number=vehicle_number,
            mechanic_on_site=mechanic_on_site,
            vehicle_location=vehicle_location,
            additional_info=additional_info,
            status='Pending'  # Set initial status
        )
        print("haii")
        booking.save()
        return render(request,'userprofile',{'booking_id': booking.id},{'service_provider': service_provider})
        

    return render(request, 'owner/main/service_request.html',{'service_provider': service_provider})  # Replace with your actual template
