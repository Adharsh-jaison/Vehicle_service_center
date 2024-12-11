from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from user.models import User,user_details,interests
from django.contrib import messages
from .models import ServiceProfile
from user.models import ChatMessage
from user.models import Booking
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
from collections import defaultdict
from user.models import Feedback



@login_required(login_url='ownerlogin')
def dashboard(request):
    try:
        service_center = ServiceProfile.objects.get(user=request.user)
    except ServiceProfile.DoesNotExist:
        # Handle the case where the user doesn't have an associated ServiceProfile
        service_center = None

    revenue_dates = []
    total_revenue = []
    if service_center:
        # Count bookings by status for the service center
        billing_count = Booking.objects.filter(service_center=service_center, status='Billing..').count()
        pending_count = Booking.objects.filter(service_center=service_center, status='Pending').count()
        accepted_count = Booking.objects.filter(service_center=service_center, status='Accepted').count()
        completed_count = Booking.objects.filter(service_center=service_center, status='Completed').count()
        paid_count = Booking.objects.filter(service_center=service_center, paid=True).count()
        unpaid_count = Booking.objects.filter(service_center=service_center, paid=False).count()

        
    if service_center:
        # Aggregate revenue by month
        revenue_data = Booking.objects.filter(service_center=service_center, paid=True)\
            .annotate(month=TruncMonth('service_date'))\
            .values('month')\
            .annotate(total_revenue=Sum('bill_amount'))\
            .order_by('month')
       
        # Prepare revenue data for chart
        for data in revenue_data:
        # Convert month number to a month name or format as needed
        #   month_name = datetime.strptime(str(data['month']), '%m').strftime('%B')
        #   revenue_dates.append(month_name)  # Append month name
          total_revenue.append(data['total_revenue'] or 0)
    else:
        # If no service center is found, set counts to 0
        billing_count = accepted_count = completed_count =paid_count = unpaid_count=pending_count=revenue_data=total_revenue=0

    context = {
        'pending_count': pending_count,
        'billing_count': billing_count,
        'accepted_count': accepted_count,
        'completed_count': completed_count,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'revenue_data': revenue_data,
        'total_revenue': total_revenue
    }
    print(total_revenue)
    
    return render(request , 'owner/main/dashboard.html',context)


def buttons(request):
    return render(request, 'owner/main/buttons.html')




import json
from textblob import TextBlob
from django.db.models import Q
def feedback_analysis(request):
    bookings = Booking.objects.filter(service_center=ServiceProfile.objects.get(user=request.user.id))
    feedback_list = Feedback.objects.filter(booking__in=bookings)
    
    # Count the ratings for service quality (1-5)
    service_quality_counts = {i: feedback_list.filter(service_quality=i).count() for i in range(1, 6)}

    # Count the professionalism ratings
    staff_professionalism_counts = [
        feedback_list.filter(staff_professionalism='Very Unprofessional').count(),
        feedback_list.filter(staff_professionalism='Unprofessional').count(),
        feedback_list.filter(staff_professionalism='Neutral').count(),
        feedback_list.filter(staff_professionalism='Professional').count(),
        feedback_list.filter(staff_professionalism='Very Professional').count(),
    ]
    did_not_meet_expectations_count = Feedback.objects.filter(expectations_met='Did Not Meet Expectations').count()
    below_expectations_count = Feedback.objects.filter(expectations_met='Below Expectations').count()
    met_expectations_count = Feedback.objects.filter(expectations_met='Met Expectations').count()
    exceeded_expectations_count = Feedback.objects.filter(expectations_met='Exceeded Expectations').count()
    far_exceeded_timeframe_count = Feedback.objects.filter(completion_timeframe='Far Exceeded Timeframe').count()
    exceeded_timeframe_count = Feedback.objects.filter(completion_timeframe='Exceeded Timeframe').count()
    met_timeframe_count = Feedback.objects.filter(completion_timeframe='Met Timeframe').count()
    under_timeframe_count = Feedback.objects.filter(completion_timeframe='Under Timeframe').count()
    expectations_met_counts = {
        1: feedback_list.filter(expectations_met=1).count(),
        2: feedback_list.filter(expectations_met=2).count(),
        3: feedback_list.filter(expectations_met=3).count(),
        4: feedback_list.filter(expectations_met=4).count(),
    }

    # Count the completion timeframe ratings (1-4)
    completion_timeframe_counts = {
        1: feedback_list.filter(completion_timeframe=1).count(),
        2: feedback_list.filter(completion_timeframe=2).count(),
        3: feedback_list.filter(completion_timeframe=3).count(),
        4: feedback_list.filter(completion_timeframe=4).count(),
    }
    
    
    # Convert counts to JSON strings
    staff_professionalism_counts_json = json.dumps(staff_professionalism_counts)
    expectations_met_counts_json = json.dumps(list(expectations_met_counts.values()))
    completion_timeframe_counts_json = json.dumps(list(completion_timeframe_counts.values()))
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Perform sentiment analysis
    for feedback in feedback_list:
        if feedback.suggestions:
            analysis = TextBlob(feedback.suggestions)
            polarity = analysis.sentiment.polarity
            
            if polarity > 0:
                positive_count += 1
            elif polarity < 0:
                negative_count += 1
            else:
                neutral_count += 1

    return render(request, 'owner/main/feedback_analysis.html', {
        'feedback_list': feedback_list,
        'staff_professionalism_counts_json': staff_professionalism_counts_json,
        'expectations_met_counts_json': expectations_met_counts_json,
        'completion_timeframe_counts_json': completion_timeframe_counts_json,
        'expectations_met_counts':expectations_met_counts,
        'staff_professionalism_counts':staff_professionalism_counts,
        'Did_Not_Meet_Expectations': did_not_meet_expectations_count,
        'Below_Expectations': below_expectations_count,
        'Met_Expectations': met_expectations_count,
        'Exceeded_Expectations': exceeded_expectations_count,
        'Far_Exceeded_Timeframe': far_exceeded_timeframe_count,
        'Exceeded_Timeframe': exceeded_timeframe_count,
        'Met_Timeframe': met_timeframe_count,
        'Under_Timeframe': under_timeframe_count,
          'bookings': bookings,  
          'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
    })










def chat(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                sender=request.user, 
                message=message_text,
                booking=booking,  # Associate the message with the current booking
                is_service_center=request.user.is_staff  # Assuming service center staff are marked as `is_staff`
            )
        return redirect('chat', booking_id=booking_id)
    if request.user.is_staff:
        base_template = 'owner/base.html'
    else:
        base_template = 'user/base.html'
    messages = booking.messages.all().order_by('timestamp')  # Fetch all messages related to the booking
    return render(request, 'owner/main/chat.html', {'messages': messages, 'booking': booking,'base_template': base_template})






@login_required
def accept_booking(request, booking_id):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Accepted'
        booking.save()
    return redirect('service_request')

@login_required
def complete_booking(request, booking_id):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Billing..'
        booking.save()
    return redirect('service_request')

def add_invoice(request, booking_id):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Billing..'
        booking.save()
    return render(request, 'owner/main/billing.html',{'booking':booking})




def add_bill(request, booking_id):
    if request.method == 'POST':
        bill_amount = request.POST.get('bill_amount')
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Save the bill amount for the booking
        booking.bill_amount = bill_amount
        booking.save()
        
        # Redirect or return a response to notify successful bill submission
        return redirect('home')
    
    return render(request, 'user/main/userprofile', {'booking': booking})





# def pay_bill(request,booking_id):
#     if request.method == 'POST':
#         booking = get_object_or_404(Booking, id=booking_id)
        
#         # Payment processing logic here (e.g., integrate payment gateway)
#         booking.paid = True  # Mark the booking as paid
#         booking.status = 'completed'  # Update the status to completed
#         booking.save()

#         return render(request,'bill_success')

#     return render(request,'user/main/feedback_form.html', {'booking': booking})





def owner_edit(request):
    print(request.user)
    if ServiceProfile.objects.filter(user=request.user).exists():
        service = ServiceProfile.objects.get(user=request.user)
    else:
        service = ServiceProfile(user=request.user)
    print(service)

    if request.method == 'POST':
        # Update address
        if request.POST['address']:
            print("adding address")
            service.address = request.POST['address']

        # Update phone number
        if request.POST['phone']:
            service.phone = request.POST['phone']

        # Update email
        if request.POST['email']:
            service.email = request.POST['email']

        # Update service center name
        if  request.POST['service_center_name']:
            service.service_center_name = request.POST['service_center_name']

        # Update operating hours
        if request.POST['operating_hours']:
            service.operating_hours = request.POST['operating_hours']

        # Update available services
        if request.POST['available_services']:
            service.available_services = request.POST['available_services']

        # Update pricing
        if request.POST['pricing']:
            service.pricing = request.POST['pricing']

        # Update ratings and reviews
        if  request.POST['ratings_reviews']:
            service.ratings_reviews = request.POST['ratings_reviews']

        # Update service center type
        if  request.POST['service_center_type']:
            service.service_center_type = request.POST['service_center_type']

        # Update facilities
        if request.POST['facilities']:
            service.facilities = request.POST['facilities']

        # Update manager name
        if  request.POST['manager_name']:
            service.manager_name = request.POST['manager_name']

        # Update booking availability
        if  request.POST['booking_availability']:
            service.booking_availability = request.POST['booking_availability']

        # Update payment methods
        if request.POST['payment_methods']:
            service.payment_methods = request.POST['payment_methods']

        if request.POST['location']:
            service.location = request.POST['location']
        
        if request.POST['vehicle_make']:
            service.vehicle_make = request.POST['vehicle_make']

        if request.FILES.get('service_center_image'):
            print(request.FILES['service_center_image'])
            service.service_center_image = request.FILES['service_center_image']

        # Handle file upload for service center image
        # if 'service_center_image' in request.FILES:
        #     serviceprofile.service_center_image = request.FILES['service_center_image']

        # Save the updated profile
        service.save()

        # Redirect to profile page after saving
        return redirect('profile')  

    # Render the service profile details
    return render(request,'owner/main/service_edit.html', {
        'serviceprofile': service
    })




def profile(request):
    if ServiceProfile.objects.filter(user=request.user).exists():
        service = ServiceProfile.objects.get(user=request.user)
    else:
        service = ServiceProfile(user=request.user)
    return render(request,'owner/main/ownerprofile.html',{
        'serviceprofile': service
    })

def profile_edit(request):
    return render(request,'owner/main/owneredit.html')
    
@login_required
def service_request(request):
    # Now request.user will always be an authenticated user
    # service_center=ServiceProfile.objects.get(user=request.user.id)
    # print(service_center)
    booking = Booking.objects.filter(service_center=ServiceProfile.objects.get(user=request.user.id))
    
    if not booking.exists():
        return render(request, 'owner/main/service_request.html', {'message': 'No bookings found.'})

    return render(request, 'owner/main/service_request.html', {'booking': booking})

def owner_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None and user.is_superuser==True :
            login(request , user)
            return render(request , 'owner/main/dashboard.html')
        elif user is None:
            msg = "Wrong credentials. Please try again!"
            return render(request , 'owner/main/login.html' , {'msg':msg})
    return render(request , 'owner/main/login.html')

def owner_logout(request):
    logout(request)
    return redirect('Login')

def status_change(request,id):
    user=User.objects.get(id=id)
    if user.is_active==True:
        user.is_active=False
    else:
        user.is_active=True
    user.save()
    return redirect("usertable")

def user_delete(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect("usertable")

def teaching_change(request,id):
    interest = interests.objects.get(id = id)
    if interest.Teaching_status == 2:
        interest.Teaching_status = 1
    elif interest.Teaching_status == 1:
        interest.Teaching_status = 2

    interest.save()
    return redirect('alerts')


  

