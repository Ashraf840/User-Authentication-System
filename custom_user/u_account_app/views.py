from django.shortcuts import render, redirect
from .forms import UserRegForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
import pdb
from .decorators import stop_authenticated_user
from home_app.decorators import stop_unauthenticated_user   # It works inspite of error-warning


# Create your views here.


@stop_authenticated_user
def userRegister(request):
    context = {
        'title': 'User Registration',
    }
    # POST request
    if request.POST:
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_account:userLogin')
        # if error occurs, show the form again
        context['register_form'] = form  # the form name, that can be called in the HTML file
    # GET request
    else:
        form = UserRegForm()
        context['register_form'] = form
    return render(request, 'u_account_app/register.html', context)


@stop_authenticated_user
def userLogin(request):
    context = {
        'title': 'User Login',
    }
    # POST request
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_address = request.POST['email']
            password = request.POST['password']
            # print("Email: %s" % (email_address))
            # print("Password: %s" % (password))
            # pdb.set_trace()
            user = authenticate(request, email=email_address, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage:home')
            # else:
            #     return redirect('user_account:userLogin')
        context['login_form'] = form  # the form name, that can be called in the HTML file
    # GET request
    else:
        form = UserLoginForm()
        context['login_form'] = form
    return render(request, 'u_account_app/login.html', context)


@stop_unauthenticated_user
def userLogout(request):
    logout(request)
    return redirect('user_account:userLogin')
