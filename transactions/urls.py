from django.urls import path
from .views import add_transaction, get_transactions, monthly_summary, category_breakdown

urlpatterns = [
    path('add/', add_transaction),
    path('list/', get_transactions),
    path('summary/', monthly_summary),
    path('category-breakdown/', category_breakdown),
]
