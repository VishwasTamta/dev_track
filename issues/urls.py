from django.urls import path
from . import views

urlpatterns = [
    path('api/issues', views.issues, name="issues"),
    path('api/reporters', views.reporters, name="reporters"),
]