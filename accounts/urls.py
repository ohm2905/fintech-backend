from django.urls import path
from .views import signup, login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]