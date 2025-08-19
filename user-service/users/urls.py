from django.urls import path
from .views import UserRegistrationView, GetCurrentUserView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('whoami/', GetCurrentUserView.as_view(), name='current-user'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
]   