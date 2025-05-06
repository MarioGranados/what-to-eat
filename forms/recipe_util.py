
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY:
    raise ValueError("API_KEY not found in environment variables.")

def get_recipes_from_api(ingredients):
    params = {
        "ingredients": ingredients,
        "number": 5,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL + "/findByIngredients", params=params)
    return response.json()

def get_recipe_by_id(recipe_id):
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL + f"/{recipe_id}/information", params=params)
    return response.json()

def generate_random_recipes():
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY,
        "number": 5
    }
    response = requests.get(BASE_URL + "/random", params=params)
    return response.json()
