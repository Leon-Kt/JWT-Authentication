from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegistrationStepOneSerializer
from users.utils import generate_verification_code, send_verification_email, generate_random_username
from verification.models import VerificationCode


class RegistrationStepOneAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationStepOneSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = generate_verification_code()

            with transaction.atomic():
                try:
                    send_verification_email(email, verification_code)
                except Exception as e:
                    return Response({'error': f'Failed to send verification email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    existing_verification_code = VerificationCode.objects.get(email=email)
                    existing_verification_code.delete()
                except ObjectDoesNotExist:
                    pass

                VerificationCode.objects.create(email=email, code=verification_code)

                request.session['registration_data'] = serializer.validated_data
                return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationStepTwoAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.session.get('registration_data', {}).get('email', None)
        verification_code = request.data.get('verification_code')

        verification_code_obj = get_object_or_404(VerificationCode, email=email, code=verification_code)

        if not verification_code_obj.is_valid():
            return Response({'error': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code_obj.email_verified = True
        verification_code_obj.save(update_fields=['email_verified'])

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)


class RegistrationStepThreeAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.session.get('registration_data', {}).get('email')
        password = request.data.get('password')

        if not email:
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code_exists = VerificationCode.objects.filter(email=email, email_verified=True).exists()
        if not verification_code_exists:
            return Response({'error': 'Email not verified'}, status=status.HTTP_400_BAD_REQUEST)

        registration_data = request.session.get('registration_data', {})
        if not registration_data:
            return Response({'error': 'Registration data not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.password_validator(password)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        username = generate_random_username()
        hashed_password = make_password(password)

        with transaction.atomic():
            User = get_user_model()
            user = User(username=username, password=hashed_password, **registration_data)
            user.save()
            request.session.pop('registration_data', None)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    def password_validator(self, password):
        min_length = 8
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters long.")
