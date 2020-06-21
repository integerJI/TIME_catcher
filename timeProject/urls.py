from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import timeUser.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', timeUser.views.signin, name='signin'),
    path('timeApp/', include('timeApp.urls')),
    path('timeUser/', include('timeUser.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
