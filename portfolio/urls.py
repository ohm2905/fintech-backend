from django.urls import path
from .views import add_stock, delete_stock, portfolio_summary

urlpatterns = [
    path('add/', add_stock),
    path('summary/', portfolio_summary),
    path('delete/<int:id>/', delete_stock),
]