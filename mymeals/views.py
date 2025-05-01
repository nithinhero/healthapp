from django.shortcuts import render, redirect
from .forms import MealForm
from .models import Meal
import requests
import base64
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # For URL reversing
from django.core.mail import send_mail
from notifications.models import Notification  # Import the Notification model
from django.contrib import messages  # O
from django.conf import settings
# API Keys (as you've already configured)
from django.conf import settings  # ✅ Use settings

# ✅ Load from settings
USDA_API_KEY = settings.USDA_API_KEY
IMAGGA_API_KEY = settings.IMAGGA_API_KEY
IMAGGA_API_SECRET = settings.IMAGGA_API_SECRET
def get_nutrients(food_name, quantity, units):
    """
    Fetches nutrient data for the given food name using USDA API.
    """
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={USDA_API_KEY}'

    try:
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
        else:
            print("USDA API response error:", response.status_code, response.text)
            return {}

        if not data.get('foods'):
            return {}

        food_data = data['foods'][0]
        nutrients = food_data.get('foodNutrients', [])
        nutrients_data = {nutrient['nutrientName']: nutrient['value'] for nutrient in nutrients}
        return nutrients_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching nutrients: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def detect_food_from_image(image_file):
    """
    Detects the food name from an uploaded image using Imagga API.
    """
    url = "https://api.imagga.com/v2/tags"

    # Encode credentials
    credentials = f"{IMAGGA_API_KEY}:{IMAGGA_API_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    files = {'image': image_file}

    try:
        response = requests.post(url, files=files, headers=headers)
        if response.status_code == 200 and response.content:
            data = response.json()
            print("Imagga API response:", data)  # Optional: Debug
        else:
            print("Imagga API error:", response.status_code, response.text)
            return ''

        tags = data.get('result', {}).get('tags', [])
        food_name = tags[0]['tag']['en'] if tags else ''
        return food_name

    except requests.exceptions.RequestException as e:
        print(f"Error detecting food from image: {e}")
        return ''
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ''


@login_required
def meal_form(request):
    """
    Handles the Meal form submission:
    - If input_type is 'image', detects food name from image
    - Fetches nutrients using USDA API
    """
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)

            # Handle food image detection
            if meal.input_type == "image" and meal.food_image:
                print("Detecting food from image...")
                meal.food_name = detect_food_from_image(meal.food_image)

            meal.save()
              # ✅ Send notification after saving meal
            Notification.objects.create(
                user=request.user,
                message=f"You submitted a meal: {meal.food_name}",
                )

            # Fetch nutrients after meal is saved
            nutrients = get_nutrients(meal.food_name, meal.quantity, meal.units)

            # Redirect to the result page after successful meal submission
            return redirect('result')  # Assuming 'meal_result' is the name of your URL pattern for the result page
    else:
        form = MealForm()

    return render(request, 'mymeals/meal_form.html', {'form': form})


@login_required
def result(request):
    """
    Displays the list of all meals and associated nutrients.
    """
    meals = Meal.objects.all().order_by('-id')

    # Attach nutrient info to each meal
    for meal in meals:
        meal.nutrients = get_nutrients(meal.food_name, meal.quantity, meal.units)

    return render(request, 'mymeals/result.html', {
        'meals': meals
    })
