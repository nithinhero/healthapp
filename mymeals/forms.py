from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['input_type', 'food_name', 'food_image', 'quantity', 'units', 'time']
        widgets = {
            'input_type': forms.RadioSelect,
            'food_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'units': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
        }
