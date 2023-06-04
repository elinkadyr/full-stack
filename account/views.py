from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from .models import MyUser
from .permissions import IsAuthorOrReadOnly
from .serializers import (ForgotPasswordSerializer, MyUserSerializer,
                          ProfileSerializer, RegisterUserSerializer,
                          ResetPasswordSerializer)
from .tasks import send_email_to_reset_password

"""вьюшка для регистрации аккаунта"""
class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались", status=201)


"""вьюшка для активации аккаунта после регистрации"""
class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect("http://localhost:3000/login")


"""вьюшка для логоута"""
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
class ProfileViewSet(mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, 
                     viewsets.GenericViewSet):
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

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)


"""вьюшка для листинга всех профилей + поиск по имени фамилии + фильтрация по языку и по группе"""
class UserListAPIView(generics.ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'last_name']
    filterset_fields = ['programming_language', 'group']

class ForgotPasswordView(APIView): 
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request, format=None):
        params = request.data
        serializer = ForgotPasswordSerializer(data=params)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = MyUser.objects.filter(email=email).first()

            if user:
                send_email_to_reset_password.delay(email)
                success_message = "We have sent you an email. Please reset your password."
                data = {"error": False, "message": success_message}
                return Response(data, status=status.HTTP_200_OK)
            else:
                error_message = "Invalid user."
                data = {"error": True, "errors": error_message}
                response_status = status.HTTP_400_BAD_REQUEST
                return Response(data, status=response_status)

        else:
            error_message = serializer.errors
            data = {"error": True, "errors": error_message}
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, status=response_status)


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer())
    def post(self, request, uid, token, format=None):
        params = request.data
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user_obj = MyUser.objects.get(pk=uid)
            if not user_obj.password and not user_obj.is_active:
                user_obj.is_active = True
                user_obj.save()
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user_obj = None

        if user_obj:
            password1 = params.get("new_password1")
            password2 = params.get("new_password2")
            if password1 != password2:
                error_message = "The two password fields didn't match."
                return Response({"error": True, "errors": error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj.set_password(password1)
                user_obj.save()
                success_message = "Password Updated Successfully. Please login."
                return Response({"error": False, "message": success_message}, status=status.HTTP_200_OK)
        else:
            error_message = "Invalid Link."
            return Response({"error": True, "errors": error_message})

