from django.urls import path
from . import views


urlpatterns = [
       path('', views.meal_form, name='meal_form'),   # Show the form
    path('result/', views.result, name='result'), 
]
