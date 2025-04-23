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

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(500))
    summary = db.Column(db.Text)
    ready_in_minutes = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    source_url = db.Column(db.String(500))
    source_name = db.Column(db.String(255))

    ingredients = db.relationship('Ingredient', backref='recipe', cascade="all, delete-orphan")
    instructions = db.relationship('Instruction', backref='recipe', cascade="all, delete-orphan")

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    original = db.Column(db.String(500))
    image = db.Column(db.String(255))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer)
    step_text = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    step_ingredients = db.relationship('StepIngredient', backref='instruction', cascade="all, delete-orphan")
    step_equipment = db.relationship('StepEquipment', backref='instruction', cascade="all, delete-orphan")

class StepIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    instruction_id = db.Column(db.Integer, db.ForeignKey('instruction.id'))

class StepEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    instruction_id = db.Column(db.Integer, db.ForeignKey('instruction.id'))



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

def get_recipe_by_id(recipe_id):
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL + f"/{recipe_id}/information", params=params)
    return response.json()

# -- Render HTML Pages --
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    return render_template('recipe.html', recipe=recipe)
# end render html pages

@app.route('/recipes', methods=['GET'])
def get_recipes():
    ingredients = request.args.get('ingredients')
    recipes = get_recipes_from_api(ingredients)
    return jsonify(recipes)

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    print('recipe_id', recipe_id)
    recipe = get_recipe_by_id(recipe_id)
    return jsonify(recipe)

@app.route('/recipes/save-recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    recipe_data = request.get_json()
    print('recipe_data')
    print(recipe_id)
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
