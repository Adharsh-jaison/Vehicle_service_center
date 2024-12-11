from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.owner_login , name="ownerlogin"),
    path('homepage',views.dashboard,name="home"),

    path('buttons', views.buttons , name="btn"),
    # path('card', views.card , name="card"),
    # path('forms', views.forms , name="forms"),
    # path('typography', views.typography , name="typography"),
    # path('usertable',views.user_table, name="usertable"),
   
    path('logout',views.owner_logout,name="Logout"),
    path('profile',views.profile,name="profile"),
    path('edit',views.profile_edit,name="edit"),
    # path('user/',include('user.urls')),
    path('teaching_change/<int:id>',views.teaching_change,name="teaching_change"),
   
    path('owner_edit',views.owner_edit,name="owner_edit"),
    path('service_request',views.service_request,name="service_request"),
    path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('complete_booking/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('add_invoice/<int:booking_id>/', views.add_invoice, name='add_invoice'),
    path('chat/<int:booking_id>/',views.chat,name="chat"),
    path('add_bill/<int:booking_id>/',views.add_bill,name="add_bill"),
    # path(' pay_bill/<int:booking_id>/',views.pay_bill,name="pay_bill"),
    path('feedback_analysis/',views.feedback_analysis,name="feedback_analysis"),
  
]