from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterUserView, ActivateView, LogoutView, ProfileViewSet


urlpatterns = [    
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()), 
    path('me/profile/', ProfileViewSet.as_view({'put': 'me', 'patch': 'me', 'delete': 'me', })), 
    path('<int:id>/profile/', ProfileViewSet.as_view({'get': 'retrieve', })),
]
