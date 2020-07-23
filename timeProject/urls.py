from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import timeApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', timeApp.views.index, name='index'),
    path('timeApp/', include('timeApp.urls')),
    path('timeUser/', include('timeUser.urls')),
]
