from django.urls import path
from django.contrib import admin
from .views import adminHandle
import os
urlpatterns = [
    path('', adminHandle),
    path('login', admin.site.urls),
    path('login/', admin.site.urls)
]
