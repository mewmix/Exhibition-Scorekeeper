#!/bin/bash

# Set the project root directory name
PROJECT_ROOT="/Users/luisocampo/Exhibition-Scorekeeper"

# Create the project directory and initial Flask app structure
mkdir -p 
$PROJECT_ROOT/{app/{static/{css,js,images},templates,models,routes,utils},tests,instance}

# Navigate into the project directory
cd $PROJECT_ROOT

# Create Python package initializers
echo "Initializing Python packages..."
touch app/__init__.py app/models/__init__.py app/routes/__init__.py 
app/utils/__init__.py tests/__init__.py

# Create main application script and other Python files
echo "Creating main application script and other Python files..."
cat <<EOF >app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main_routes, auth_routes, game_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(game_routes)

    return app
EOF

# Create a basic config file
cat <<EOF >config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 
'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
EOF

# Create placeholder route files
echo "Creating placeholder route files..."
echo "from flask import Blueprint" >app/routes/main_routes.py
echo "from flask import Blueprint" >app/routes/auth_routes.py
echo "from flask import Blueprint" >app/routes/game_routes.py

# Create placeholder model file
echo "from app import db" >app/models/models.py

# Create utility files
echo "Creating utility files..."
touch app/utils/game_logic.py

# Create placeholder template and static files
echo "<h1>Hello, PoolScorekeeper!</h1>" >app/templates/index.html
touch app/static/css/style.css
touch app/static/js/main.js

# Create a simple test file
echo "import unittest" >tests/test_basic.py

# Create a requirements.txt file
echo "Creating requirements.txt file..."
cat <<EOF >requirements.txt
Flask
Flask-SQLAlchemy
Flask-Login
Flask-Migrate
Flask-WTF
Flask-Cors
EOF

# Create a .flaskenv file for environment variables
echo "Creating .flaskenv file..."
cat <<EOF >.flaskenv
FLASK_APP=run.py
FLASK_ENV=development
EOF

# Create the main run file
echo "Creating the main run file..."
cat <<EOF >run.py
from app import create_app, db
from app.models.models import User, Game  # Adjust imports based on your 
models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game}  # Adjust based on your 
models
EOF

echo "Project structure created successfully. Navigate into $PROJECT_ROOT 
and activate your virtual environment to proceed."

