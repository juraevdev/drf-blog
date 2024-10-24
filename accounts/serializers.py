from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser, UserConfirmation, PasswordReset
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Confirmation password didn't match")
        
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exist")
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exist")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            is_active = False
        )
        code = user.generate_verify_code(self)
        return {
            'message': 'Verification code is sent to your email. Please check your Inbox!',
            'code': code
        }
    
class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=5, max_length=5)

class ResendVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


    def validate(self, data):
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords didn't match")
        return data
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('email')
        return super().validate(attrs)