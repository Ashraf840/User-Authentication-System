from django.shortcuts import render


# Create your views here.
# PROJECT INDEX PAGE ("HOME PAGE") IS CREATED HERE
def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'home_app/index.html', context)
