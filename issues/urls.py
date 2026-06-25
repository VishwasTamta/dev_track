from django.urls import path
from . import views

urlpatterns = [
    path('api/issues/', views.create_issue, name="create_issue")
]