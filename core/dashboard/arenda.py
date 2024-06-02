from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchall, dictfetchone

from base.helper import user_home, date_hisob_kitob, admin_permission_check
from core.models import Arenda, Car, Card
from datetime import datetime as dt


@login_required(login_url='login')
def arenda_olish(request, car_id):
    if request.POST:

        if request.user.user_type != 2:
            return render(request, 'base.html', {"error": 404})
        car = Car.objects.filter(id=car_id, status=True).first()
        if not car:
            return render(request, 'base.html', {"error": 404})
        son = int(request.POST.get('day', 1))
        # arenda yaratish

        Arenda.objects.create(user=request.user, car=car, date_to=date_hisob_kitob(son), summa=car.price * son,
                              pay_type='Plastik')

        request.session['success'] = "Moshinani Arendaga olish uchun adminga xabar yuborildi. Admin Javobini kuting"
        request.session['tries'] = 1
    return redirect('home')


@admin_permission_check
def arenda_list(request):
    sql = """
    select ar.*, us.fio, cc.name, cc.raqam, cc.price, cc.yili from core_arenda ar
    inner join core_user us on us.id = ar.user_id
    inner join core_car cc on cc.id = ar.car_id 
    order by ar.status asc, ar.id DESC
    
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)
        print(result)

    return render(request, 'pages/arenda.html', {'arendalar': result})


@admin_permission_check
def manage_arenda(request, pk, status):
    if status == 1:
        arenda = Arenda.objects.filter(id=pk).first()
        if not arenda or arenda.status in [2, 3]:
            request.session['error'] = "Arenda mavjud emas yoki mumkin bulmagan holat"
            request.session['a-tries'] = 1
            return redirect('arenda-list')
        card = Card.objects.filter(owner=arenda.user).first()
        if not card or card.balance < arenda.summa:
            request.session['error'] = "Carta yo\'q yoki balance yetarli emas !"
            request.session['a-tries'] = 1
            return redirect('arenda-list')
        car = Car.objects.filter(id=arenda.car_id, status=True).first()
        if not car:
            request.session['error'] = "Mashina mavjud emas yoki band  "
            request.session['a-tries'] = 1
            return redirect('arenda-list')

        card.balance -= arenda.summa
        card.save()

        car.status = False
        car.save()

        arenda.status = 1
        arenda.save()
        return redirect('arenda-list')
    elif status == 2:
        arenda = Arenda.objects.filter(id=pk).first()
        if not arenda or arenda.status in [2, 3]:
            request.session['error'] = "Arenda mavjud emas yoki mumkin bulmagan holat"
            request.session['a-tries'] = 1
            return redirect('arenda-list')
        car = Car.objects.filter(id=arenda.car_id, status=False).first()
        if not car:
            request.session['error'] = "Mashina mavjud emas yoki band  "
            request.session['a-tries'] = 1
            return redirect('arenda-list')

        car.status = True
        car.save()
        arenda.status = 2
        arenda.save()
        return redirect('arenda-list')
    elif status == 3:
        arenda = Arenda.objects.filter(id=pk).first()
        if not arenda or arenda.status in [2, 3]:
            request.session['error'] = "Arenda mavjud emas yoki mumkin bulmagan holat"
            request.session['a-tries'] = 1
            return redirect('arenda-list')
        arenda.status = 3
        arenda.save()

    return redirect('arenda-list')


def arenda_view(request):
    sql = """
    SELECT sum(summa)  as jami
    from core_arenda ca 
    WHERE status = 1
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

    return render(request, 'pages/arenda.html', {'summa': result})
