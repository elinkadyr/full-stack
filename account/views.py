from django.shortcuts import get_object_or_404, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView


from .models import MyUser
from .permissions import IsAuthorOrReadOnly
from .serializers import RegisterUserSerializer, ProfileSerializer


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



"""вьюшка для профиля пользователя"""
class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser]

    def get_object(self):
        if self.action == 'me':
            user = self.request.user
        else:
            user_id = self.kwargs['id']
            user = MyUser.objects.get(pk=user_id)
        self.check_object_permissions(self.request, user)
        return user

    @action(["put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)