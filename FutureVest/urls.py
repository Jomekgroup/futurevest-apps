from django.contrib import admin
from django.urls import path, include  # include for app urls

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('', include('investor.urls')),  # Main app 'investor' urls
]
