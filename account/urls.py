from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (RegisterUserView, 
                    ActivateView, 
                    LogoutView, 
                    ProfileViewSet, 
                    UserListAPIView,
                    ForgotPasswordView,
                    ResetPasswordView, 
                    TopUpBillingView)


urlpatterns = [    
    path('register/', RegisterUserView.as_view(), name='account-register'),
    path('activate/<str:activation_code>/', ActivateView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('me/profile/', ProfileViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me', 'delete': 'me', })), 
    path('<int:id>/profile/', ProfileViewSet.as_view({'get': 'retrieve', })),
    path('profiles/', UserListAPIView.as_view(), name='user-listing'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('billing/top-up/', TopUpBillingView.as_view()),
]

