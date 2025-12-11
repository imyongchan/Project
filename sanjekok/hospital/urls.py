from django.urls import path
from . import views

app_name = "Hospital"

urlpatterns = [
    path("", views.hospital_search, name="hospital_search"),
    path("api/", views.hospital_api, name="hospital_api"),
    path("geocode/", views.hospital_geocode, name="hospital_geocode"),
    path("detail/<str:hospital_id>/", views.hospital_detail, name="hospital_detail"),
]
