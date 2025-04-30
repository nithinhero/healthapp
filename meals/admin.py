from django.contrib import admin
from .models import Meal

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_type', 'food_name', 'quantity', 'units', 'time', 'created_at')
    list_filter = ('input_type', 'time', 'units')
    search_fields = ('food_name',)
