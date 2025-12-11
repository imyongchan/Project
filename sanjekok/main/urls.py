from django.urls import path
from . import views

app_name = 'Main'

urlpatterns = [
    path("", views.main, name='main'),
    path("service/", views.service, name='service'),
    path("tech/", views.tech, name='tech'),
]
