from django.urls import path

from core.dashboard.arenda import arenda_olish, arenda_list, manage_arenda, arenda_view
from core.dashboard.auth import sign_in, sign_out, manage_user, change_password, user_profile, top_up_user, \
    add_card_to_user
from core.dashboard.cars import manage_cars, manage_brand_and_ctg, car_filter
from core.dashboard.view import index, profile

urlpatterns = [
    # auth
    path('', index, name="home"),
    path('login/', sign_in, name="login"),
    path('logout/', sign_out, name="logout"),
    path('user-profile/<int:user_id>/', user_profile, name="user-profile"),
    path('top/up/<int:user_id>/', top_up_user, name="top-up-user"),
    path('add/card/user/<int:user_id>/', add_card_to_user, name="add-to-user"),


    # users
    path("users/<int:ut>/", manage_user, name="users"),
    path("users/<int:ut>/add/<status>/", manage_user, name="users-add"),
    path("users/<int:ut>/edit/<status>/<int:pk>/", manage_user, name="users-edit"),
    path("users/chp/<int:user_id>/", change_password, name="users-chp"),
    path('profile/', profile, name='profile'),

    # cars
    path("cars/", manage_cars, name="cars"),
    path("cars/form/<status>/", manage_cars, name="cars-add"),
    path("cars/edit/<status>/<int:pk>/", manage_cars, name="cars-edit"),
    path("cars/filter/<key>/<int:pk>/", car_filter, name="cars-filter"),


    # brand
    path('<key>-crud/', manage_brand_and_ctg, name='ctg_brand_list'),
    path('<key>-crud/edit/<int:pk>/', manage_brand_and_ctg, name='ctg_brand_edit'),
    path('<key>-crud/delete/<int:pk>/<int:delete>/', manage_brand_and_ctg, name='ctg_brand_del'),


    # arenda
    path('arenda/<int:car_id>/', arenda_olish, name='arenda'),
    path('arenda/list/', arenda_list, name='arenda-list'),
    path('arenda/pk-<int:pk>/st-<int:status>/', manage_arenda, name='arenda-manage'),
    path('arenda/view/', arenda_view, name='arenda-view'),



]


