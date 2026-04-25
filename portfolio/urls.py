from django.urls import path
from .views import add_stock, portfolio_summary

urlpatterns = [
    path('add/', add_stock),
    path('summary/', portfolio_summary),
]