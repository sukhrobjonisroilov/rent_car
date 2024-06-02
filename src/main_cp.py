def main(request):
    result = {}
    path = request.path.replace("/", " ").replace('-', " ").split()
    if path:
        path = path[0]
    else:
        path = 'nothing'
    sidebars = {
        "users": 'users_active',
        "cars": "cars_active",
        'ctg': "ctg_active",
        'brand': "brand_active",
        'profile': "profile_active",
    }.get(path, 'nothing')

    result.update({sidebars: 'active'})
    # check qiberadi
    if request.session.get('tries', 0) <= 0:
        try:
            del request.session['success']
            del request.session['tries']
        except:
            pass
    else:
        request.session['tries'] = request.session['tries'] - 1

    if request.session.get('a-tries', 0) <= 0:
        try:
            del request.session['error']
            del request.session['a-tries']
        except:
            pass
    else:
        request.session['a-tries'] = request.session['a-tries'] - 1

    return result
