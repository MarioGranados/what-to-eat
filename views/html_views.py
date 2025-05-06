from flask import Blueprint, render_template
from models import Meal, MealPlan, Recipe, Ingredient
import requests
import os


html_views = Blueprint('html_views', __name__)
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

@html_views.route('/')
def home():
    res = requests.get(BASE_URL + "/random", params={"number": 5, "apiKey": API_KEY})
    return render_template('index.html', recipes=res.json().get('recipes', []))

@html_views.route('/<int:recipe_id>')
def recipe_detail(recipe_id):
    res = requests.get(BASE_URL + f"/{recipe_id}/information", params={"apiKey": API_KEY})
    return render_template('recipe.html', recipe=res.json())

@html_views.route('/saved-recipes')
def saved_recipes():
    return render_template('saved-recipes.html', recipes=Recipe.query.all())

@html_views.route('/ingredients')
def current_ingredients():
    return render_template('ingredients.html', ingredients=Ingredient.query.all())

@html_views.route('/meal-plans/<int:plan_id>', methods=['GET'])
def view_meal_plan(plan_id):
    plan = MealPlan.query.get(plan_id)

    if not plan:
        return "Meal plan not found", 404
    
    meal_recipes = {}  
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    meal_types = ['Breakfast', 'Lunch', 'Dinner']
    
    for day in days_of_week:
        meal_recipes[day] = {}
        for meal_type in meal_types:
            meal = Meal.query.filter_by(day=day, meal_type=meal_type, meal_plan_id=plan.id).first()
            meal_recipes[day][meal_type] = meal.recipe 
    
    return render_template('meal_plan.html', 
                           start_date=plan.start_date, 
                           end_date=plan.end_date, 
                           days_of_week=days_of_week, 
                           meal_types=meal_types, 
                           meal_recipes=meal_recipes,
                           meal_plan=plan)

