from django.views.generic.base import TemplateView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse, name='browse'),
]