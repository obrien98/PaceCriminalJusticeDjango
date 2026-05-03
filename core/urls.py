from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.index, name = "index"),
    path("gallery/", core_views.gallery_list, name="gallery_list"),
    path("events/", core_views.event_list, name="event_list"),
    path("events/<int:event_id>/", core_views.event_detail, name="event_detail"),

]
