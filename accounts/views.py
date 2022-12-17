from django.shortcuts import render

from accounts.serializers import (
    LoginSeralizer,
)

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
# Create your views here.


class LoginApiView(GenericAPIView):
    serializer_class = LoginSeralizer


    def post(self, request, *args, **kwargs):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
        
