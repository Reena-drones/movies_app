from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
#from .models import User
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from uuid import uuid4
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # user,email,password validator
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user = None
        print('validate',data)
        # if the email has been passed
        if '@' in email:
            user = User.objects.filter(
                Q(email=email)).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=email)
            if user.check_password(password):
                return data
            else:
                raise ValidationError("User credentials are not correct.")

    def get_user(self, data):
        email = data.get("email", None)
        user = User.objects.get(email=email)
        return user

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data


    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff', 'auth_token')

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass
