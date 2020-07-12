from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('mypage/', views.userinfo, name='mypage'),
    path('profile_update', views.ProfileUpdateView.as_view(), name='profile_update'),
]
