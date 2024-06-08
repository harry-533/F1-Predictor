from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("driver/<str:driverId>/<str:trackId>", views.driver, name="driver"),
    path("race/<str:trackId>", views.race, name="race")
]
