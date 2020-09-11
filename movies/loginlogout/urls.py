from django.urls import path
from .views import Record, Login, Logout
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', Record, name="register"),
    path('login/', Login, name="login"),
    path('logout/', Logout, name="logout"),
    path('api-token-auth/', views.obtain_auth_token)
]
