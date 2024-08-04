from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from users.utils import email_exists, username_exists


class EmailExistsAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return JsonResponse({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'email_exists': email_exists(email)})


class UsernameExistsAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return JsonResponse({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'username_exists': username_exists(username)})
