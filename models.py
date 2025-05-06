from extensions import db 


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

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    meals = db.relationship('Meal', backref='meal_plan', cascade="all, delete-orphan")

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe')
