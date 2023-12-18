
from django.contrib import admin
from django.urls import path, include

from myappF23 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('myappF23.urls')),
]