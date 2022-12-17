from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class LoginSeralizer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password','email','refresh_token','access_token']
    

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error":"Invalid Creditials"})
        if not user.is_active:
            raise serializers.ValidationError({"error":"Sorry! cannot login deactivte account."})
        tokens = user.get_tokens()
        return {
            'email':user.email,
            'username':user.username,
            'refresh_token':tokens['refresh'],
            'access_token':tokens['access'],
        }
    
