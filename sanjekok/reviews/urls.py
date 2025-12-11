from django.urls import path
from . import views

app_name = 'Reviews'

urlpatterns = [
    path("create/", views.review_create, name="review_create"),
    path("list/<int:hospital_id>/", views.review_list, name="review_list"),
]
