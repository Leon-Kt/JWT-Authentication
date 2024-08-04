from django.contrib.auth import logout, login
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken as SimpleJWTRefreshToken

from refresh_tokens.utils import get_refresh_token_object_from_db_by_user_id
from users.utils import get_user_by_user_id


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_public_path(request.path):
            print(request.path)
            return self.get_response(request)

        access_token = self.get_access_token(request)
        if access_token:
            try:
                return self.authenticate_using_access_token(request, access_token)
            except TokenError as e:
                print('Error with Access Token:', e)

        return self.authenticate_using_refresh_token(request)

    def is_public_path(self, path):
        public_paths = [
            '/login',
            '/api/login/',
            '/api/register/',
            '/api/logout/',
            '/admin',
            '/favicon.ico',
        ]
        return any(path.startswith(p) for p in public_paths)

    def get_access_token(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            print('access token available', request.path)
            return access_token
        print('Could not get access token', request.path)

    def authenticate_using_access_token(self, request, access_token):
        user_id = self.get_user_id_from_access_token(access_token)
        user = get_user_by_user_id(user_id)
        if user.is_authenticated:
            print('authenticated', request.path)
            login(request, user)
            request.user = user
            return self.get_response(request)
        print('user not authenticated', request.path)

    def get_refresh_token(self, user_id):
        refresh_token = get_refresh_token_object_from_db_by_user_id(user_id)
        if refresh_token:
            print('refresh token available')
            return refresh_token
        print('Could not get refresh token')

    def validate_refresh_token(self, refresh_token):
        try:
            SimpleJWTRefreshToken(refresh_token)
            print('validated refresh token')
            return True
        except TokenError as e:
            print('Error with Refresh Token:', e)
            return False

    def authenticate_using_refresh_token(self, request):
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            print("no user_id in cookies")
            return self.redirect_to_login_if_not_anonymous(request)

        refresh_token = self.get_refresh_token(user_id)
        if not refresh_token or not self.validate_refresh_token(refresh_token):
            return self.redirect_to_login_if_not_anonymous(request)

        if self.is_refresh_token_blacklisted(refresh_token):
            print("Refresh token is blacklisted")
            return self.redirect_to_login_if_not_anonymous(request)

        user = get_user_by_user_id(user_id)
        response = self.get_response(request)
        new_access_token = self.generate_and_set_new_access_token(user, response)
        self.authenticate_using_access_token(request, new_access_token)
        request.user = user
        return response

    def is_refresh_token_blacklisted(self, refresh_token):
        try:
            return SimpleJWTRefreshToken(refresh_token).blacklisted
        except Exception as e:
            print('Error in blacklist function', e)
            return False

    def redirect_to_login_if_not_anonymous(self, request):
        if not request.user.is_anonymous:
            print('make anonymous')
            logout(request)

        print(request.user.is_anonymous)
        print('Redirecting to login page')
        if request.path == '/':
            return redirect('login')
        return Response({'message': 'unauthenticated', 'status': 'unauthorized', 'data': None}, status=401)

    def generate_and_set_new_access_token(self, user, response):
        new_access_token = AccessToken.for_user(user)
        response.set_cookie('access_token', str(new_access_token), httponly=True, secure=False)
        return str(new_access_token)

    def get_user_id_from_access_token(self, access_token):
        return AccessToken(access_token).payload.get('user_id')
