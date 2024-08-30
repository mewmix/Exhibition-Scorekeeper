from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.utils.logging_config import configure_logging

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='../templates', static_folder='../static')
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    configure_logging(app)

    with app.app_context():
        from app.models import Player, GameState  # Import models after initializing the extensions
        db.create_all()

    from app.routes.auth import auth_bp
    from app.routes.game import game_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    return app
