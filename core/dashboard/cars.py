from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from base.helper import admin_permission_check, user_home
from core.forms.cars import CarForm
from core.models import Category, Brand, Car


@admin_permission_check
def manage_brand_and_ctg(request, key, pk=None, delete=0):
    try:
        Model = {
            "ctg": Category,
            'brand': Brand
        }[key]
    except:
        return render(request, 'base.html', {"error": 404})
    root = Model()
    if pk:
        root = Model.objects.filter(pk=pk).first()
        if delete:
            root.delete()
            return redirect('ctg_brand_list', key=key)
    if request.POST:
        root.name = request.POST.get('name')
        root.save()
        return redirect('ctg_brand_list', key=key)

    roots = Model.objects.all().order_by('-pk')
    paginator = Paginator(roots, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    ctx = {
        "roots": result,
        'key': key,
        'p_title': "Kategoriyalar" if key == 'ctg' else "Brendlar",
    }
    return render(request, f'pages/ctg.html', ctx)


@login_required(login_url='login')
def car_filter(request, key, pk):
    try:
        Model = {
            "ctg": Category,
            'brand': Brand
        }[key]
    except:
        return render(request, 'base.html', {"error": 404})
    root = Model.objects.filter(id=pk).first()
    if not root:
        return render(request, 'base.html', {"error": 404})

    cars = Car.objects.filter(**{key: root})
    paginator = Paginator(cars, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)

    ctx = user_home(request)
    ctx['cars'] = result
    ctx['root'] = root

    return render(request, 'pages/user_home.html', ctx)


@admin_permission_check
def manage_cars(request, pk=None, delete=0, status=None):
    root = None
    if pk:
        root = Car.objects.filter(pk=pk).first()
        if delete:
            root.delete()
            return redirect('cars')
    form = CarForm(request.POST or None, request.FILES or None, instance=root)
    if form.is_valid():
        form.save()
        return redirect('cars')
    roots = Car.objects.all().order_by('-pk')
    paginator = Paginator(roots, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    ctx = {
        "roots": result,
        'p_title': "Cars",
        "form": form,
        "status": status
    }
    return render(request, 'pages/cars.html', ctx)
