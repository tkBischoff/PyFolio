from django.urls import path

from . import views

urlpatterns = [
    path('buy/<ticker>/', views.buy_security, name='buy_security'),
]
