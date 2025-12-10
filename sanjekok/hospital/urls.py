from django.urls import path
from . import views

urlpatterns = [
    path("", views.hospital_search, name="hospital_search"),
    path("api/", views.hospital_api, name="hospital_api"),
    path("detail/<str:objt_id>/", views.hospital_detail, name="hospital_detail"),
]
