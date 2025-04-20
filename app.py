import requests
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import dotenv 
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()


# Database Stuff
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False, unique=True)  # Unique to avoid duplicates
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "name": self.name
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

# Ingredient Model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Unique to avoid duplicates
    quantity = db.Column(db.Integer, nullable=False)



API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables.")
BASE_URL = os.getenv('BASE_URL')
BY_INGREDIENTS = os.getenv('BY_INGREDIENTS')
BY_ID = os.getenv('BY_ID')


#GET https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2

ingredients = 'apples, flour, sugar' # this is how the variable should look like


def get_recipes_from_api(ingredients):
    params = {
        "ingredients": ingredients,
        "number": 5,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL + f"/findByIngredients", params=params)
    #return jsonify(response.json()) # did not work for some reason
    return response.json()  # Return JSON response directly

def get_individual_recipe_info(recipe_id):
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL + f"/{recipe_id}/information", params=params)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = get_individual_recipe_info(recipe_id)
    return render_template('recipe.html', recipe=recipe)


@app.route('/recipes', methods=['GET'])
def get_recipes():
    ingredients = request.args.get('ingredients')
    recipes = get_recipes_from_api(ingredients)
    return jsonify(recipes)

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    print('recipe_id', recipe_id)
    recipe = get_individual_recipe_info(recipe_id)
    return jsonify(recipe)

@app.route('/recipes/save-recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    recipe_data = request.get_json()
    recipe = Recipe(recipe_id=recipe_id, name=recipe_data['name'])
    print(recipe)
    recipe.save()
    return jsonify({"message": "Recipe saved successfully!"}), 201

@app.route('/recipes/delete-recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe deleted successfully!"}), 200
    else:
        return jsonify({"message": "Recipe not found!"}), 404
    
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
