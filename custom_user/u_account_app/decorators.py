from django.shortcuts import redirect


def stop_authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
