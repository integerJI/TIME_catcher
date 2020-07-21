from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('timesave/', views.timesave, name='timesave'),
    path('calender/', views.calender, name='calender'),
    path('notices/', views.notices, name='notices'),
]