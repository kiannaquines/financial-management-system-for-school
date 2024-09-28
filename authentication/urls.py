from django.urls import path
from authentication.views import *

urlpatterns = [
    path('',auth_index_page, name='login'),
    path('register/',auth_register_page, name='register'),
]