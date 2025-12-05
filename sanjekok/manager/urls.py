from django.urls import path
from . import views

app_name = 'Manager'

urlpatterns = [
    path("", views.login, name='login'),
    path("main/", views.main, name='main'),
    path("dash/", views.dash, name='dash')
]
