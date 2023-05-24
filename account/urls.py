from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

from .views import RegisterUserView, ActivateView, LogoutView, ProfileViewSet


router = DefaultRouter()
router.register("profile", ProfileViewSet)


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]
