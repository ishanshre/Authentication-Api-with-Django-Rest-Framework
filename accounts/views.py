from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from accounts.email import create_email
from accounts.tokens import decode_token
from accounts.serializers import (
    LoginSeralizer,
    RegisterSerializer,
    EmailVerifySerializer,
)

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
# Create your views here.

User = get_user_model()
class LoginApiView(GenericAPIView):
    serializer_class = LoginSeralizer


    def post(self, request, *args, **kwargs):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
        


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        current_site = get_current_site(request=request).domain
        create_email(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            action="email_verify",
            current_site=current_site
        )
        return Response(
            {
                "done": serializer.data,
                "message":"please check your email to verify your email address",
            }, status=status.HTTP_201_CREATED
        )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerifySerializer
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        token = request.GET.get("token")
        username, verify_status = decode_token(token)
        if verify_status:
            user = get_object_or_404(User, username=username)
            user.email_confirmed = True
            user.save()
            return Response({
                "done":"email verified"}, status=status.HTTP_200_OK
            )
        return Response({
            "error":"invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)

