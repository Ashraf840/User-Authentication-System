from django.shortcuts import redirect


def stop_unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('homepage:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
