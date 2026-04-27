from django.urls import path
from .views import add_transaction, get_transactions, monthly_summary, category_breakdown,add_category,get_categories, delete_transaction, delete_category,overall_summary,update_transaction

urlpatterns = [
    path('add/', add_transaction),
    path('', get_transactions),
    path('summary/', monthly_summary),
    path('category-breakdown/', category_breakdown),
    path('add-category/', add_category),
    path('categories/', get_categories),
    path('delete/<int:id>/', delete_transaction),
    path('delete-category/<int:id>/', delete_category),
    path('summary/overall/', overall_summary),
    path('update/<int:pk>/', update_transaction),
]
