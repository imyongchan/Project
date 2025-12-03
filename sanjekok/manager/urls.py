from django.urls import path
from . import views

app_name = 'Manager'

urlpatterns = [
    path("", views.manager_main, name='manager')
]
