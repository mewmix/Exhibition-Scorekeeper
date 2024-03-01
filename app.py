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
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    game_type = db.Column(db.String(50))  # To store '8ball' or '9ball'
    current_state = db.Column(db.Text)  # Serialized game state
    status = db.Column(db.String(50), default='in_progress')  # e.g., 'in_progress', 'finished'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])


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
    match_sn_history = db.Column(db.Text)  # JSON-encoded string or consider a separate model for history
    racks_to_win = db.Column(db.Integer)
    inning_total = db.Column(db.Integer)
    matches_played = db.Column(db.Integer)
    matches_won = db.Column(db.Integer)
    win_percentage = db.Column(db.Float)
    racks_won = db.Column(db.Integer)
    points_total = db.Column(db.Integer)
    points_per_match = db.Column(db.Float)
    points_available = db.Column(db.Float)
    defensive_shot_total = db.Column(db.Integer)
    defensive_shot_average = db.Column(db.Float)
    eight_on_the_break = db.Column(db.Integer)
    break_and_run = db.Column(db.Integer)
    mini_slam = db.Column(db.Integer)

class NineballStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    skill_level = db.Column(db.Integer)
    # Include other fields as per the JSON structure
    match_sn_history = db.Column(db.Text)  # JSON-encoded string or consider a separate model for history
    points_to_win = db.Column(db.Integer)
    inning_total = db.Column(db.Integer)
    matches_played = db.Column(db.Integer)
    matches_won = db.Column(db.Integer)
    win_percentage = db.Column(db.Float)
    match_ball_count = db.Column(db.Integer)
    points_total = db.Column(db.Integer)
    points_per_match = db.Column(db.Float)
    points_available = db.Column(db.Float)
    defensive_shot_total = db.Column(db.Integer)
    defensive_shot_average = db.Column(db.Float)
    nine_on_the_snap = db.Column(db.Integer)
    break_and_run = db.Column(db.Integer)
    mini_slam = db.Column(db.Integer)


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
        # Assuming Player model has 'id' and 'name' fields
        players = Player.query.with_entities(Player.id, Player.name).all()
        player_data = [{'id': player.id, 'name': player.name} for player in players]
    else:
        # User is not logged in, handle accordingly
        # For example, you might redirect them to the login page
        return redirect(url_for('login'))
    
    return render_template('index.html', players=player_data)


    # User is not logged in, redirect to the login page
    return redirect(url_for('login'))



@app.route('/game/start', methods=['POST'])
def start_game():
    player1_id = request.form.get('player1_id')
    player2_id = request.form.get('player2_id')
    game_type = request.form.get('game_type')

    # Validate player IDs and game type
    if not player1_id or not player2_id or player1_id == player2_id or game_type not in ['8ball', '9ball']:
        return jsonify({'error': 'Invalid request'}), 400

    player1 = Player.query.get(player1_id)
    player2 = Player.query.get(player2_id)
    if not player1 or not player2:
        return jsonify({'error': 'Player not found'}), 404

    # Prevent starting a new game if one is already in progress
    existing_game = GameState.query.filter(
        ((GameState.player1_id == player1_id) & (GameState.player2_id == player2_id)) |
        ((GameState.player1_id == player2_id) & (GameState.player2_id == player1_id)),
        GameState.status == 'in_progress',
        GameState.game_type == game_type
    ).first()

    if existing_game:
        return jsonify({'error': 'A game between these players is already in progress'}), 400

    # Initialize the game object dynamically based on game type
    game = EightballGame() if game_type == '8ball' else NineballGame()
    serialized_game = game.to_json()

    new_game_state = GameState(
        player1_id=player1_id,
        player2_id=player2_id,
        game_type=game_type,
        current_state=serialized_game,
        status='in_progress'
    )
    db.session.add(new_game_state)
    db.session.commit()

    return jsonify({'message': f'{game_type.title()} game started', 'game_id': new_game_state.id}), 201

@app.route('/game/stats/<int:game_id>', methods=['GET'])
def game_stats(game_id):
    game_state = GameState.query.get(game_id)

    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    # Ensure the requesting user is a participant
    user_id = session.get('user_id')
    if game_state.player1_id != user_id and game_state.player2_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    # Deserialize the game state
    game_state_dict = json.loads(game_state.current_state)
    # Additional processing could be done here based on game_type if necessary

    return jsonify(game_state_dict)
@app.route('/current_matches')
def current_matches():
    if 'user_id' not in session:
        # Ensure there's a user session; otherwise, redirect or handle error appropriately
        return 'You must be logged in to view matches', 403

    user_id = session['user_id']
    matches = GameState.query.filter(
        (GameState.player1_id == user_id) | (GameState.player2_id == user_id),
        GameState.status == 'in_progress'
    ).all()

    # Construct HTML options for the select dropdown
    options_html = ''.join([f'<option value="{match.id}">{match.player1.name} vs {match.player2.name} - {match.game_type}</option>' for match in matches])

    return options_html


@app.route('/game_action_form/<int:match_id>')
def game_action_form(match_id):
    game_state = GameState.query.get_or_404(match_id)
    # Assuming you have a specific form template for each game type
    form_template = f"{game_state.game_type}_form.html"
    return render_template(form_template, match_id=match_id)


@app.route('/game/action', methods=['POST'])
def game_action():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    match_id = request.form.get('match_id')
    action = request.form.get('action')
    ball_number = request.form.get('ball_number', type=int, default=None)

    game_state_record = GameState.query.filter_by(id=match_id).first()
    if not game_state_record:
        return jsonify({'error': 'Match not found'}), 404

    # Dynamically determine game type from the game_state_record
    game_type = game_state_record.game_type  # This assumes you have a game_type field in GameState

    if action not in ['pocket_ball', 'switch_turn', 'end_game']:
        return jsonify({'error': 'Invalid action'}), 400

    # Instantiate the correct game object based on game type
    if game_type == '8ball':
        current_game = EightballGame.from_json(game_state_record.current_state)
    elif game_type == '9ball':
        current_game = NineballGame.from_json(game_state_record.current_state)
    else:
        return jsonify({'error': 'Invalid game type'}), 400

    try:
        if action == 'pocket_ball' and ball_number is not None:
            valid_ball = (1 <= ball_number <= 15 if game_type == '8ball' else 1 <= ball_number <= 9)
            if not valid_ball:
                return jsonify({'error': 'Invalid ball number for the game type'}), 400
            current_game.ball_pocketed(ball_number)
        elif action == 'switch_turn':
            current_game.switch_turn()
        elif action == 'end_game':
            current_game.end_game()

        game_state_record.current_state = current_game.to_json()
        db.session.commit()

        return jsonify({
            'message': 'Action processed successfully',
            'current_game_state': json.loads(game_state_record.current_state)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process action', 'details': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
