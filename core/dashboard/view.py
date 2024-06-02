from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base.helper import counter, user_home
from core.models import Card


@login_required(login_url='login')
def index(request):
    if request.user.user_type == 1:
        return render(request, 'pages/index.html', {'count': counter()})

    return render(request, 'pages/user_home.html', user_home(request))


@login_required(login_url='login')
def profile(request):
    card = Card.objects.filter(owner=request.user).first()
    ctx = {
        'user': request.user,
        "card": card,
    }
    return render(request, 'pages/profile.html', ctx)
