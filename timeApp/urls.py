from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('timesave/', views.timesave, name='timesave'),
    path('calender/', views.calender, name='calender'),
    path('notices/', views.notices, name='notices'),
    path('customer/', views.customer, name='customer'),
    path('notices_create/', views.notices_create, name='notices_create'),
    path('customer_create/', views.custome_creater, name='customer_create'),
]