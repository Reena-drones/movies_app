from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from .models import Movies
#from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['Get'])
@permission_classes([IsAuthenticated])
def Dashboard(request):
    context = {}
    if(request.session.get('user_data')):
        print('dta inside home',request.session.get('user_data'))
    movies = Movies.objects.all()
    context['movies'] = movies
    print("ooooooooooo", request.data)
    return render(request, 'dashboard.html', context)




@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    print(request.headers)
    return render(request, 'watch.html')