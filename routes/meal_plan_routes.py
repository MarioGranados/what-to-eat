from flask import Blueprint, request, jsonify
from models import db, MealPlan, Meal, Recipe
import random
from datetime import date, timedelta

meal_plan_routes = Blueprint('meal_plan_routes', __name__)

@meal_plan_routes.route('/meal-plans', methods=['POST'])
def create_meal_plan():
    today = date.today()
    start_date = today
    end_date = today + timedelta(days=5)

    plan = MealPlan(
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(plan)
    db.session.flush() 

    saved_recipes = Recipe.query.all()

    if not saved_recipes:
        return jsonify({'message': 'You need atleast 5 recipes to generate a meal plan'}), 400

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    meal_types = ['Breakfast', 'Lunch', 'Dinner']

    for day in days_of_week:
        for meal_type in meal_types:
            recipe = random.choice(saved_recipes)
            db.session.add(Meal(
                day=day, 
                meal_type=meal_type,
                recipe_id=recipe.id, 
                meal_plan_id=plan.id
            ))

    db.session.commit()
    return jsonify({'message': 'Meal plan created'}), 201

@meal_plan_routes.route('/meal-plans', methods=['GET'])
def get_meal_plans():
    plans = MealPlan.query.all()
    return jsonify([{
        'id': p.id, 
        'start_date': str(p.start_date), 
        'end_date': str(p.end_date),
        'meals': [{
            'day': m.day, 
            'meal_type': m.meal_type, 
            'recipe_title': m.recipe.title
        } for m in p.meals]
    } for p in plans])

@meal_plan_routes.route('/meal-plans/delete/<int:plan_id>', methods=['DELETE'])
def delete_meal_plan(plan_id):
    plan = MealPlan.query.get(plan_id)
    if not plan:
        return jsonify({'message': 'Not found'}), 404
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
