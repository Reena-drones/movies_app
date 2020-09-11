from django.urls import include, path
from .views import Dashboard, get_watchlist

urlpatterns = [
    path('home/', Dashboard, name="home"),
    path('watch/', get_watchlist, name="watchlist"),
]
