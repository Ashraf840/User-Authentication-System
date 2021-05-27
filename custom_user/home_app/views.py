from django.shortcuts import render
from .decorators import stop_unauthenticated_user


# Create your views here.
# PROJECT INDEX PAGE ("HOME PAGE") IS CREATED HERE
def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'home_app/index.html', context)


@stop_unauthenticated_user
def secretPage(request):
    context = {
        'title': 'Secret Page',
    }
    return render(request, 'home_app/secretpage.html', context)
