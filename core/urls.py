from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.index, name = "index"),
    path("events/<int:event_id>/", core_views.event_detail, name="event_detail"),

]
