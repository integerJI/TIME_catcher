from django.urls import path
from . import views

urlpatterns = [
    path('mobile/', views.mobile, name='mobile'),
    path('index/', views.index, name='index'),
    path('timesave/', views.timesave, name='timesave'),
    path('calender/', views.calender, name='calender'),
    path('notices/', views.notices, name='notices'),
    path('customer/', views.customer, name='customer'),
    path('notices_create/', views.notices_create, name='notices_create'),
    path('customer_create/', views.customer_create, name='customer_create'),
    path('customer_save/', views.customer_save, name='customer_save'),
    path('customer_detail/<int:customer_id>', views.customer_detail, name='customer_detail'),
    path('customer_update/<int:customers_id>', views.customer_update, name='customer_update'),
]