from flask import Flask, request, session, jsonify, render_template, url_for, redirect, make_response
from flask_cors import CORS
import json
import time
from core.scrimage_scorekeeper import EightballGame, NineballGame, PlayerStats
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # For password hashing
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scorekeeper.db'
app.config['SECRET_KEY'] = 'MOOOCOWMOOOOOO'

db = SQLAlchemy(app)
CORS(app)
bcrypt = Bcrypt(app)


def load_player_names():
    players = Player.query.with_entities(Player.name).all()
    return [player.name for player in players]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
