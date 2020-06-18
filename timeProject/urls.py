from django.contrib import admin
from django.urls import path, include
import timeUser.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', timeUser.views.login, name='login'),
    path('timeApp/', include('timeApp.urls')),
    path('timeUser/', include('timeUser.urls')),
]
