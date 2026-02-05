from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('kenkou/', include('kenkou.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
