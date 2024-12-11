from django.urls import path
from . import views 

urlpatterns=[
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('Login' , views.user_login , name="Login"),
    path('courses',views.courses, name="course"),
    path('register' , views.user_register , name="user_register"),
    path('success',views.success,name='success'),
    path('userprofile',views.user_profile,name='userprofile'),
    path('logout',views.user_logout,name='logout'),
    # path('lists/<str:sub>',views.lists,name="lists"),
    path('useredit',views.user_edit,name="useredit"),
    # path('feedback',views.user_feedback,name="feedback"),
    # path('teach/<int:id>',views.teach_noti,name="teach_noti"),
    # path('change/<int:id>/<str:sub>',views.change,name="change"),
    path('thanks',views.thanks,name="thanks"),
    # path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    # user_contact_info
    # path('user_edit',views.user_edit,name='user_edit'),
    path('search_service',views.search_service,name='search_service'),
    path('user_book/<int:service_provider_id>/',views.user_book,name="user_book"),
    path('book_service/', views.book_service, name='book_service'),
    path('bill_success/',views.bill_success,name='bill_success'),
    path('feedback/<int:booking_id>/', views.feedback_form, name='feedback_form'),
    path('feedback_view/', views.feedback_view, name='feedback_view'),
    path(' pay_bill/<int:booking_id>/',views.pay_bill,name="pay_bill"),
    
    # path('user_booking_display/',views.user_booking_display,name="user_booking_display"),
]