import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from methodism import generate_key

from base.helper import permission_check, admin_permission_check, create_unique_number
from core.forms.auth import UserForm
from core.models import User, Card


def sign_in(request):
    if request.POST:
        pas = request.POST.get("pass")
        username = request.POST.get("username")
        print(username,"$$$$$$$$$$$$$$$$$$$$")
        user = User.objects.filter(username=username).first()

        if not user:
            return render(request, 'auth/login.html', {"error": "username or Password error"})
        if not user.check_password(pas):
            return render(request, 'auth/login.html', {"error": "username or Password error"})
        if not user.is_active:
            return render(request, 'auth/login.html', {"error": "Bu Foydalanuvchi qora ro'yxatda"})

        login(request, user)
        return redirect('home')
    return render(request, 'auth/login.html')


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('login')


@admin_permission_check
def manage_user(request, ut, pk=None, status='list'):
    user = User.objects.filter(pk=pk).first() or None
    form = UserForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        user = form.save()
        if status == 'add':
            user.set_password(request.POST.get('password'))
            user.save()
            today = datetime.date.today()
            data = {
                "owner": user,
                "name": "Rent Card",
                "number": create_unique_number(),
                "expire": today.strftime(f"%m/{str(today.year + 1)[2:]}"),  # 11/23 -> 11/24
                "balance": 50_000,
                "token": uuid.uuid4()
            }
            Card.objects.create(**data)
        return redirect('users', ut=ut)
    else:
        print(form.errors)
    ctx = {
        "users": User.objects.filter(user_type=ut),
        "form": form,
        "status": status,
        "ut": ut,
        "user": user

    }
    return render(request, 'pages/users.html', ctx)


@permission_check
def change_password(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if request.POST:
        if user == request.user:
            request.user.set_password(request.POST.get('password'))
            request.user.save()
        else:
            user.set_password(request.POST.get('password'))
            user.save()
    return redirect('users', ut=user.user_type)


@admin_permission_check
def user_profile(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return render(request, "base.html", {'error': 404})
    card = Card.objects.filter(owner=user).first()
    ctx = {
        "card": card,
        "user": user
    }
    return render(request, 'pages/user-profile.html', ctx)


@admin_permission_check
def top_up_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return render(request, "base.html", {'error': 404})
    if request.POST:
        card = Card.objects.filter(owner=user).first()
        if card:
            card.balance += int(request.POST.get('bonus', 0))
            card.save()
    return redirect('user-profile', user_id=user_id)


@admin_permission_check
def add_card_to_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return render(request, "base.html", {'error': 404})
    card = Card.objects.filter(owner=user).first()
    if not card:
        today = datetime.date.today()
        data = {
            "owner": user,
            "name": "Rent Card",
            "number": create_unique_number(),
            "expire": today.strftime(f"%m/{str(today.year + 1)[2:]}"),  # 11/23 -> 11/24
            "balance": 50_000,
            "token": uuid.uuid4()
        }
        Card.objects.create(**data)

    return redirect('user-profile', user_id=user_id)
