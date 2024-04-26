from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                try:
                    validate_password(value, instance)
                except ValidationError as e:
                    raise serializers.ValidationError(e)
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value