# from django.shortcuts import render

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import authenticate
# from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
# from django.contrib.auth.models import User

# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully!", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 return Response({"message": "Login successful!", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
#             return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

# Dictionary to store OTPs temporarily
otp_storage = {}

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP
            otp = random.randint(100000, 999999)
            otp_storage[user.email] = otp

            # Send OTP via Email
            send_mail(
                "Verify Your Email",
                f"Your OTP for verification is {otp}",
                "your_email@gmail.com",  # Sender Email
                [user.email],  # Receiver Email
                fail_silently=False,
            )

            return Response({"message": "User registered! Check email for OTP."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if email in otp_storage and otp_storage[email] == int(otp):
            user = User.objects.filter(email=email).first() 
            if user:
                user.is_active = True
                user.save()
                del otp_storage[email]  # Remove OTP after successful verification
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 return Response({"message": "Login successful!", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
#             return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
