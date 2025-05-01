from django.db import models
from datetime import datetime

def get_default_meal_time():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return 'morning'
    elif 12 <= current_hour < 18:
        return 'afternoon'
    else:
        return 'evening'

# Example: Top 100 common foods (shortened list here)
FOOD_NAME_CHOICES = [
    ('apple', 'Apple'),
    ('banana', 'Banana'),
    ('rice', 'Rice'),
    ('chicken', 'Chicken'),
    ('egg', 'Egg'),
    ('bread', 'Bread'),
    ('milk', 'Milk'),
    ('carrot', 'Carrot'),
    ('potato', 'Potato'),
    ('orange', 'Orange'),
    ('broccoli', 'Broccoli'),
    ('cheese', 'Cheese'),
    ('yogurt', 'Yogurt'),
    ('beef', 'Beef'),
    ('tofu', 'Tofu'),
    ('fish', 'Fish'),
    ('pasta', 'Pasta'),
    ('spinach', 'Spinach'),
    ('tomato', 'Tomato'),
    ('cucumber', 'Cucumber'),
    ('grapes', 'Grapes'),
    ('mango', 'Mango'),
    ('pineapple', 'Pineapple'),
    ('watermelon', 'Watermelon'),
    ('nuts', 'Nuts'),
    # Add more as needed up to 100
]


class Meal(models.Model):
    INPUT_CHOICES = [
        ('name', 'Food Name'),
        ('image', 'Food Image'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    UNITS_CHOICES = [
    ('g', 'Grams'),
    ('kg', 'Kilograms'),
    ('mg', 'Milligrams'),
    ('lb', 'Pounds'),
    ('oz', 'Ounces'),
    ('ml', 'Milliliters'),
    ('l', 'Liters'),
    ('cup', 'Cups'),
    ('tbsp', 'Tablespoons'),
    ('tsp', 'Teaspoons'),
    ('piece', 'Pieces'),
    ('slice', 'Slices'),
    ('bowl', 'Bowls'),
    ('plate', 'Plates'),
    ('serving', 'Servings'),
    ('can', 'Cans'),
    ('pack', 'Packs'),
    ('bottle', 'Bottles'),
]


    input_type = models.CharField(max_length=10, choices=INPUT_CHOICES)
    food_name = models.CharField(max_length=255, choices=FOOD_NAME_CHOICES, blank=True, null=True)
    food_image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    quantity = models.FloatField()
    units = models.CharField(max_length=10, choices=UNITS_CHOICES)
    time = models.CharField(max_length=20, choices=TIME_CHOICES, default=get_default_meal_time)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_name if self.food_name else f"Meal {self.id}"
