import random
from contextlib import closing

from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import redirect, render
from methodism import dictfetchone

from core.models import Category, Car, Brand
from datetime import datetime as dt


def permission_check(funk):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        if not request.user.is_staff or not request.user.is_superuser:
            return render(request, "base.html", {'error': 404})
        if request.user.user_type != 1:
            return render(request, "base.html", {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


def admin_permission_check(funk):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        if request.user.user_type != 1:
            return render(request, "base.html", {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


def card_mask(number):
    number = number.replace(" ", "")
    return f"{number[:4]} **** **** {number[-4:]}"


def generate_number():
    return "5614 " + " ".join(str(random.randint(1000, 9999)) for x in range(3))


def create_unique_number():
    number = generate_number()
    with open("base/card_number.txt", 'r') as file:
        if not number in file.read().split("\n"):
            with open("card_number.txt", "a") as write_file:
                write_file.write(f"{number}\n")
            return number
    return create_unique_number()


def counter():
    sql = '''
    select 
    ( select COUNT(*) from core_car) as car,
    (select COUNT(*) from core_arenda) as arend,
    (select COUNT(*) from core_user us WHERE us.user_type=1) as admin,
    (select COUNT(*) from core_user us WHERE us.user_type=2) as costumer
    from core_user
    limit 1
    '''
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        natija = dictfetchone(cursor)
    return natija


def user_home(request):
    roots = Car.objects.filter(status=True).order_by('-pk')
    paginator = Paginator(roots, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    return {
        "ctgs": Category.objects.all().order_by('-pk'),
        "brands": Brand.objects.all().order_by('-pk'),
        "cars": result,

    }


def date_hisob_kitob(son: int):
    today_day = int(dt.today().strftime(f"%d"))
    today_oy = int(dt.today().strftime(f"%m"))
    today_yil = int(dt.today().strftime(f"%Y"))

    sum_days = int(son) + int(today_day)
    if sum_days > 30:
        today_oy += 1
        sum_days -= 30

    if today_oy > 12:
        today_oy -= 12
        today_yil += 1

    if sum_days < 10:
        natija = f"{today_yil}-{'0' if today_oy < 10 else ''}{today_oy}-0{sum_days}"
    else:
        natija = f"{today_yil}-{today_oy}-{sum_days}"

    to = dt.today().strftime(natija)
    return to


