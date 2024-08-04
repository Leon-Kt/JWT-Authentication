from rest_framework import serializers

from users.models import User


class RegistrationStepOneSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField()

    class Meta:
        model = User
        fields = ['name', 'email', 'birthdate']

    def validate_birthdate(self, value):
        try:
            return value.isoformat()
        except AttributeError:
            raise serializers.ValidationError('Invalid date format')
