from django.contrib import admin
from .models import Car,User
# Register your models here.
from core.models.users import SanctionedIndividual

admin.site.register(Car)
admin.site.register(User)
admin.site.register(SanctionedIndividual)
