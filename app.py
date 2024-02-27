from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import CORS
import json
import time 
# Assuming scrimage_scorekeeper.py is correctly set up and accessible
from scrimage_scorekeeper import EightballGame, NineballGame, PlayerStats
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_bcrypt import Bcrypt  # For password hashing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scorekeeper.db'
app.config['SECRET_KEY'] = 'MOOOCOWMOOOOOO'

db = SQLAlchemy(app)
CORS(app)
bcrypt = Bcrypt(app)



class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_name = db.Column(db.String(100))
    player2_name = db.Column(db.String(100))
    current_state = db.Column(db.Text) 

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    lags_won = db.Column(db.Integer, default=0)
    # Relationship to detailed stats
    eightball_stats = db.relationship('EightballStats', backref='player', lazy=True)
    nineball_stats = db.relationship('NineballStats', backref='player', lazy=True)

class EightballStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    skill_level = db.Column(db.Integer)
    # Include other fields as per the JSON structure
    match_sn_history = db.Column(db.Text)  # JSON-encoded string or consider a separate model for history

class NineballStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    skill_level = db.Column(db.Integer)
    # Include other fields as per the JSON structure
    points_history = db.Column(db.Text)  # JSON-encoded string or consider a separate model for history

def load_player_names():
    players = Player.query.with_entities(Player.name).all()
    return [player.name for player in players]




# Signup/Register Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user input from the form
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if the username already exists in the database
        existing_user = Player.query.filter_by(name=name).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = Player(name=name, password=hashed_password)

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    # Render the signup form
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the form
        name = request.form.get('name')
        password = request.form.get('password')

        # Query the database for the user
        user = Player.query.filter_by(name=name).first()

        # Check if the user exists and if the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Set the user ID in the session
            session['user_id'] = user.id
            return redirect(url_for('home'))  # Redirect to the home page after login

        return jsonify({'error': 'Invalid username or password'}), 401

    # Render the login form
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    # Clear the user ID from the session
    session.pop('user_id', None)
    return redirect(url_for('home'))  # Redirect to the home page after logout

# Home Route (Protected)
@app.route('/')
def home():
    # Check if the user is logged in
    if 'user_id' in session:
        # User is logged in, load the index page
        player_names = load_player_names()
        return render_template('index.html', players=player_names)

    # User is not logged in, redirect to the login page
    return redirect(url_for('login'))


@app.route('/game/start', methods=['POST'])
def start_game():
    player1_name = request.form.get('player1')
    player2_name = request.form.get('player2')

    # Check for existing game between these two players
    existing_game = GameState.query.filter(
        GameState.player1_name.in_([player1_name, player2_name]),
        GameState.player2_name.in_([player1_name, player2_name]),
        GameState.current_state != 'finished'  # Assuming 'finished' is a state you set when the game is over
    ).first()

    if existing_game:
        return jsonify({'error': 'A game between these players is already in progress'}), 400

    game = EightballGame(player1_name, player2_name)
    # Assuming EightballGame has a method to serialize its state to JSON
    serialized_game = game.to_json()
 

    new_game_state = GameState(
        player1_name=player1_name,
        player2_name=player2_name,
        current_state=serialized_game
    )
    db.session.add(new_game_state)
    db.session.commit()

    # Return the game ID
    return jsonify({'message': f'Game started between {player1_name} and {player2_name}', 'game_id': new_game_state.id}), 201


@app.route('/game/stats/<int:game_id>', methods=['GET'])
def game_stats(game_id):
    # Get the game state from the database based on the provided game ID
    game_state = GameState.query.get(game_id)

    if game_state:
        # Deserialize the game state JSON string to a dictionary
        game_state_dict = json.loads(game_state.current_state)
        return jsonify(game_state_dict)
    else:
        return jsonify({'error': 'Game not found'}), 404


@app.route('/player/create', methods=['POST'])
def create_player():
    # Retrieve form data or JSON data
    name = request.form.get('name') or request.json.get('name')
    lags_won = request.form.get('lags_won', 0) or request.json.get('lags_won', 0)

    # Create a new Player instance
    new_player = Player(name=name, lags_won=int(lags_won))
    db.session.add(new_player)
    db.session.commit()

    return jsonify({'message': f"Player profile created for {name}"}), 201

@app.route('/game/action', methods=['POST'])
def game_action():
    # Get the action and other relevant data from the request
    action = request.form.get('action')
    ball_number = int(request.form.get('ball_number'))

    # You can add more data fields as needed based on the type of action

    # Retrieve the latest game state from the database
    latest_game_state = GameState.query.order_by(GameState.id.desc()).first()

    if not latest_game_state:
        return jsonify({'error': 'No game in progress'}), 404

    # Deserialize the game state JSON string to a dictionary
    game_state_dict = json.loads(latest_game_state.current_state)

    # Instantiate the game object using the deserialized game state dictionary
    current_game = EightballGame.from_json(json.dumps(game_state_dict))

    # Handle different actions based on the request
    if action == 'pocket_ball':
        # Perform logic to handle pocketing a ball
        current_game.ball_pocketed(ball_number)
    elif action == 'switch_turn':
        # Perform logic to switch the turn
        current_game.switch_turn()
    elif action == 'end_game':
        # Perform logic to end the game
        current_game.end_game()

    # Update the game state in the database
    latest_game_state.current_state = current_game.to_json()
    db.session.commit()

    return jsonify({'message': 'Action processed'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
