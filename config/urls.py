
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
    path('', include('portal.urls')),
    path('api/v1/', include('api.urls')),
]
