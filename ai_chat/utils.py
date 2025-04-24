import requests
import openai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get keys securely
USDA_API_KEY = os.getenv('USDA_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY


def query_usda_api(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        'query': query,
        'api_key': USDA_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('foods'):
            first_item = data['foods'][0]
            return f"Name: {first_item['description']}\nCalories: {first_item.get('foodNutrients', [{}])[0].get('value', 'N/A')}"
    return None


def fallback_ai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query}
            ]


        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I couldn't process our query right now."
