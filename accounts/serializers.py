from rest_framework import serializers
from rest_framework.settings import api_settings

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import Profile


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
    


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']

    
    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if len(username) < 4:
            raise serializers.ValidationError({"error":"username must be of length more than 4"})
        if not username.isalnum():
            raise serializers.ValidationError({"error":"username must be combination of letters and number or letters only"})
        if password != confirm_password:
            raise serializers.ValidationError({"error":"password and confirm password does not match"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error":"username already exists"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":"email already exists"})
        user = User(username=username, email=email)
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                "password": serializers_error[api_settings.NON_FIELD_ERRORS_KEY]
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []


class ResendEmailConfirmationLinkSerailzer(serializers.ModelSerializer):
    email_confirmed = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['email_confirmed']
        

class SimpleUserSerializer(serializers.ModelSerializer):
    email_confirmed = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ['username','email','email_confirmed']



class UserDetailSerailizer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    email_confirmed = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','email_confirmed','is_active','date_joined','last_login']


class ProfileSeralizer(serializers.ModelSerializer):
    user = UserDetailSerailizer()

    class Meta:
        model = Profile
        fields = ['user','avatar','bio','gender','facebook','twitter','github']