from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if 'member_id' not in request.session:
            messages.error(request, "로그인이 필요합니다.")
            return redirect('Member:login')
        return function(request, *args, **kwargs)
    return wrap
