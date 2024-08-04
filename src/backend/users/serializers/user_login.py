from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        if not username_or_email or not password:
            raise serializers.ValidationError("Both username/email and password are required")

        return attrs
