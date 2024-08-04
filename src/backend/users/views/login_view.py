from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken as SimpleJWTRefreshToken

from refresh_tokens.models import RefreshToken
from users.serializers import UserLoginSerializer


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        username_or_email = validated_data.get("username_or_email")
        password = validated_data.get("password")

        user = self.custom_authenticate(username_or_email, password)

        if user is None:
            return Response({"error": "Invalid username/email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        try:
            print("check if there is already a Refresh token")
            existing_refresh_token = RefreshToken.objects.get(user_id=user.id)
            print("try to delete existing Token")
            existing_refresh_token.delete()
        except ObjectDoesNotExist:
            print("there is no already existing refresh token")
            pass

        print("create new refresh token")
        refresh = SimpleJWTRefreshToken.for_user(user)
        refresh_token = RefreshToken.objects.create(
            user_id=user.id,
            token=str(refresh)
        )

        print("create new access token")
        access_token = str(refresh.access_token)

        response = JsonResponse({
            "msg": "Login Success",
            "access_token": access_token,
            "refresh_token_id": refresh_token.id
        }, status=status.HTTP_200_OK)

        access_token_cookie_expiration = timezone.now() + settings.ACCESS_TOKEN_COOKIE_LIFETIME
        response.set_cookie('access_token', access_token, httponly=True, secure=False, expires=access_token_cookie_expiration)  # In Produktionsumgebung secure auf True setzen
        response.set_cookie('user_id', user.id, httponly=True, secure=False, expires=timezone.now() + timedelta(weeks=9999))

        return response

    def custom_authenticate(self, username_or_email: str, password: str):
        if '@' in username_or_email:
            kwargs = {'email': username_or_email}
        else:
            kwargs = {'username': username_or_email}

        User = get_user_model()
        try:
            user = User.objects.get(**kwargs)
            if check_password(password, user.password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
