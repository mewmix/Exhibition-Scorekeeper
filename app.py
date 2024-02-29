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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = Player.query.filter_by(name=name).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            # This else block ensures a response is provided if credentials don't match
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        # This covers the case for a GET request
        return render_template('login.html')
8

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
    game_type = request.form.get('game_type')  # New line to get the game type from the request

    # Check for existing game between these two players
    existing_game = GameState.query.filter(
        GameState.player1_name.in_([player1_name, player2_name]),
        GameState.player2_name.in_([player1_name, player2_name]),
        GameState.current_state != 'finished'
    ).first()

    if existing_game:
        return jsonify({'error': 'A game between these players is already in progress'}), 400

    if game_type == '8ball':
        game = EightballGame(player1_name, player2_name)
    elif game_type == '9ball':
        game = NineballGame(player1_name, player2_name)  # Assuming NineballGame is similar to EightballGame
    else:
        return jsonify({'error': 'Invalid game type specified'}), 400

    serialized_game = game.to_json()

    new_game_state = GameState(
        player1_name=player1_name,
        player2_name=player2_name,
        current_state=serialized_game
    )
    db.session.add(new_game_state)
    db.session.commit()

    return jsonify({'message': f'Game started between {player1_name} and {player2_name}', 'game_id': new_game_state.id, 'game_type': game_type}), 201

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
    # Validate action
    action = request.form.get('action')
    game_type = request.form.get('game_type')  # Get game type from the request
    valid_actions = ['pocket_ball', 'switch_turn', 'end_game']
    
    if action not in valid_actions:
        return jsonify({'error': 'Invalid action'}), 400
    if game_type not in ['8ball', '9ball']:
        return jsonify({'error': 'Invalid game type'}), 400
    
    ball_number = None
    if action == 'pocket_ball':
        try:
            ball_number = int(request.form.get('ball_number'))
            if ball_number < 1 or (ball_number > 15 and game_type == '8ball') or (ball_number > 9 and game_type == '9ball'):
                raise ValueError
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid ball number'}), 400

    latest_game_state = GameState.query.order_by(GameState.id.desc()).first()
    if not latest_game_state:
        return jsonify({'error': 'No game in progress'}), 404

    game_state_dict = json.loads(latest_game_state.current_state)

    # Instantiate the game object based on the game type
    if game_type == '8ball':
        current_game = EightballGame.from_json(json.dumps(game_state_dict))
    elif game_type == '9ball':
        current_game = NineballGame.from_json(json.dumps(game_state_dict))

    try:
        message = 'Action processed'
        if action == 'pocket_ball':
            current_game.ball_pocketed(ball_number)
            message = 'Ball pocketed successfully'
        elif action == 'switch_turn':
            current_game.switch_turn()
            message = 'Turn switched'
        elif action == 'end_game':
            current_game.end_game()
            message = 'Game ended'

        latest_game_state.current_state = current_game.to_json()
        db.session.commit()

        response = {
            'message': message,
            'current_turn': current_game.current_turn,
        }
        return jsonify(response)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process action', 'details': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
