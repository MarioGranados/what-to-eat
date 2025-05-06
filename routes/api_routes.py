from flask import Blueprint, jsonify, request
from models import db, Recipe, Ingredient, Instruction, StepIngredient, StepEquipment
import requests
import os

from forms.recipe_util import (
    get_recipes_from_api,
    get_recipe_by_id,
)


api_routes = Blueprint('api_routes', __name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

@api_routes.route('/recipes', methods=['GET'])
def get_recipes():
    ingredients = request.args.get('ingredients')
    recipes = get_recipes_from_api(ingredients)
    return jsonify(recipes)

@api_routes.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    return jsonify(get_recipe_by_id(recipe_id))

@api_routes.route('/recipes/save-recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    data = get_recipe_by_id(recipe_id)

    recipe = Recipe(
        title=data['title'], image=data['image'], summary=data['summary'],
        ready_in_minutes=data['readyInMinutes'], servings=data['servings'],
        source_url=data['sourceUrl'], source_name=data['sourceName']
    )
    db.session.add(recipe)
    db.session.flush()

    for ing in data['extendedIngredients']:
        db.session.add(Ingredient(name=ing['name'], original=ing['original'],
                                  image=ing['image'], recipe_id=recipe.id))

    for step in data['analyzedInstructions'][0]['steps']:
        instruction = Instruction(step_number=step['number'], step_text=step['step'], recipe_id=recipe.id)
        db.session.add(instruction)
        db.session.flush()
        for ing in step.get('ingredients', []):
            db.session.add(StepIngredient(name=ing['name'], image=ing['image'], instruction_id=instruction.id))
        for eq in step.get('equipment', []):
            db.session.add(StepEquipment(name=eq['name'], image=eq['image'], instruction_id=instruction.id))

    db.session.commit()
    return jsonify({"message": "Recipe saved!"}), 201

@api_routes.route('/recipes/delete-recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'message': 'Not found'}), 404
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Deleted!'}), 200
