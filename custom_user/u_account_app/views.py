from django.shortcuts import render, redirect
from .forms import UserRegForm


# Create your views here.
def userRegister(request):
    context = {
        'title': 'User Registration',
    }
    # # POST request
    # if request.POST:
    #     form = UserRegForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('login')
    #     # if error occurs, show the form again
    #     context['register-form'] = form
    # # GET request
    # else:
    #     form=UserRegForm()
    #     context['register-form'] = form
    return render(request, 'u_account_app/register.html', context)

