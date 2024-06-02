from django import forms

from core.models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'