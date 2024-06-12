from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import random
import datetime
from .models import AUser  
from .util import send_otp  
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializers



class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if not phone:
            return Response("Phone number is required", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AUser.objects.get(phone=phone)
        except ObjectDoesNotExist:
            user = AUser.objects.create(phone=phone)

        if int(user.max_otp_try) == 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
            return Response("Max OTP try reached, try after an hour", status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP and update user record
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(user.max_otp_try) - 1

        user.otp = otp
        user.otp_expiry = otp_expiry

        if max_otp_try == 0:
            user.otp_max_out = timezone.now() + datetime.timedelta(hours=1)
            user.max_otp_try = 0  # If max try reached, set to 0 until otp_max_out passes
        elif max_otp_try < 0:
            user.max_otp_try = 3  # Reset after block period
            user.otp_max_out = None
        else:
            user.max_otp_try = max_otp_try
            user.otp_max_out = None

        user.save()
        send_otp(user.phone, otp, user)

        return Response("Successfully generated OTP", status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
 permission_classes = [AllowAny]
 def post(self, request, *args, **kwargs):
    otp = request.data['otp']
    print(otp)
    user = AUser.objects.get(otp=otp)
    if user:
        login(request, user)
        user.otp = None
        user.otp_expiry = None
        user.max_otp_try = 3
        user.otp_max_out = None
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
    else:
        return Response("Please enter the correct OTP", status=status.HTTP_400_BAD_REQUEST)