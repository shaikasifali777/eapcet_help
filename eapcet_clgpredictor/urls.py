from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.display_form),
    path("visualize/",views.charts_data)
]
