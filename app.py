from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

import models

from routes.api_routes import api_routes
from routes.meal_plan_routes import meal_plan_routes
from views.html_views import html_views

app.register_blueprint(api_routes)
app.register_blueprint(meal_plan_routes)
app.register_blueprint(html_views)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
