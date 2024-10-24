import random
import datetime
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from accounts.models import CustomUser, UserConfirmation, PasswordReset
from accounts.serializers import (
    RegisterSerializer, 
    RegisterVerifySerializer, 
    ResendVerifyCodeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)

# Create your views here.
class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.create(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)
    
class RegisterVerifyApiView(generics.GenericAPIView):
    serializer_class = RegisterVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            code = serializer.data['code']
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            otp_code = UserConfirmation.objects.filter(code=code).first()
            if not otp_code or otp_code.is_used or otp_code.expires < timezone.now():
                return Response({'message': 'Code is expires or invalid'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            otp_code.is_used = True
            user.save()
            otp_code.save()
            return Response({'message': 'code is valid and user activated'})
        return Response(serializer.errors)
    
class ResendVerifyCodeApiView(generics.GenericAPIView):
    serializer_class = ResendVerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'message': 'User not found'})
        code = user.generate_verify_code(request)
        return Response({'code':code})
    
class PasswordResetRequestApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
            code = ''.join([str(random.randint(0, 100)%10) for _ in range(5)])
            PasswordReset.objects.create(
                user = user,
                code = code,
                expires = timezone.now() + datetime.timedelta(minutes=2)
            )
            return Response({'message': 'Password reset code sent to your email. Check your inbox',
                             'code': code})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            code = serializer.data['code']
            new_password = serializer.data['new_password']

            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            reset = PasswordReset.objects.filter(user=user, code=code, is_used=False).first()
            if reset is None or reset.expires < timezone.now():
                return Response({'message': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            reset.is_used = True
            reset.save()

            return Response({'message': 'Password successfully reset'})
        return Response(serializer.errors)
    