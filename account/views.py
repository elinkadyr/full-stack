from django.shortcuts import get_object_or_404, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError

from .models import MyUser
from .serializers import ProfileSerializer, RegisterUserSerializer


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались", status=201)


class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect("http://34.125.13.20/")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                TokenRefreshView().blacklist_token(refresh_token)
            except TokenError:
                return Response({'detail': 'Недействительный токен аутентификации или истек срок действия.'}, status=400)
        return Response({'detail': 'Вы успешно вышли из системы.'}, status=200)

    

class ProfileViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = ProfileSerializer

