"""
    Serializer for User
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from validate_email import validate_email

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    """Checking given email is unique"""
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()), validate_email
        ])
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        """Create a new user"""
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def validate_phone_number(self, value):
        """Check that the phone number is unique across all users."""
        if value and User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Phone number already exists.')
        return value

    def update(self, instance, validated_data):
        """Update existing user with the validated data"""
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Wrong password.')
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def validate_new_password(self, value):
        if value == self.initial_data['old_password']:
            raise serializers.ValidationError('New password cannot be the same as the old password.')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
