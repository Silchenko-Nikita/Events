from django.urls import path
from accounts.api import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
]
