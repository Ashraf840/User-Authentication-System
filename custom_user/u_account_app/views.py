from django.shortcuts import render, redirect
from .forms import UserRegForm


# Create your views here.
def userRegister(request):
    context = {
        'title': 'User Registration',
    }
    # POST request
    if request.POST:
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage:home')
        # if error occurs, show the form again
        context['register_form'] = form     # the form name, that can be called in the HTML file
    # GET request
    else:
        form = UserRegForm()
        context['register_form'] = form
    return render(request, 'u_account_app/register.html', context)
