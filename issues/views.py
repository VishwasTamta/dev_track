from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from issues.models import Reporter, Issue
from .api.issues import create_issue
from .api.reporters import reporters



