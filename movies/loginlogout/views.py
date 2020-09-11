from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, AuthUserSerializer
from movie_rating.views import Dashboard
from movie_rating.models import Movies
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout

@api_view(['GET', 'POST'])
def Record(request):
    context = {}
    if(request.method == 'GET'):
        queryset = User.objects.all()
        queryset = User.objects.all()
        serializer_class = UserLoginSerializer(queryset, context={'request': request}, many=True)
        serializer_class = UserSerializer(queryset, context={'request': request}, many=True)
        context['registration_form']= serializer_class.data
        return render(request, 'register.html', context)

    elif request.method == 'POST':
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = AuthUserSerializer(user).data
            context['token'] = data.get('auth_token')
            return render(request, 'login.html', context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def Login(request):
    context = {}
    if(request.method == 'GET'):
        queryset = User.objects.all()
        serializer_class = UserLoginSerializer(queryset, context={'request': request}, many=True)
        context['login_form']= serializer_class.data
        print(context, request.user.is_authenticated)
        return render(request, 'login.html', context)

    elif request.method == 'POST':
        serializer_class = UserLoginSerializer(data=request.data)
        try:
            if serializer_class.is_valid(raise_exception=True):
                print('pathetic',serializer_class.data)
                user = serializer_class.get_user(serializer_class.data)
                data = AuthUserSerializer(user).data
                print(data)
                print(data.get('auth_token'))
                account = authenticate(email=request.data.get('email'), password=request.data.get('password'))
                context['token'] = data.get('auth_token')
                response = render(request, 'login.html', context)
                response['authorization'] = 'Token ' + data.get('auth_token')
                response["Access-Control-Allow-Methods"]  = "GET, POST, OPTIONS"
                response["Access-Control-Allow-Headers"]= "access-control-allow-origin"
                response["Access-Control-Allow-Credentials"] =  "Origin, Content-Type, Accept"
                return response
        except Exception as e:
            print(e)
            context['login_form']= serializer_class.errors
            context['status']= HTTP_400_BAD_REQUEST
            return render(request, 'login.html', context)


@api_view(['POST'])
def Logout(request):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer(queryset, context={'request': request}, many=True)

    if request.method == 'POST':
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    context = {}
    movies = Movies.objects.all()
    context['movies'] = movies
    return render(request, 'index.html', context)