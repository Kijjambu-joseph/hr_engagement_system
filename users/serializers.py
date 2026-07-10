"""Serializers for the users auth endpoints."""

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'region_cluster', 'branch_name', 'employee_id')
        read_only_fields = fields


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'region_cluster', 'branch_name', 'employee_id')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            attrs['user'] = User.objects.get(pk=attrs['user_id'])
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({'user_id': 'User not found.'}) from exc
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()



