from flask import Flask, request, session, jsonify, render_template, url_for, redirect, make_response
from flask_cors import CORS
import json
import time
from scrimage_scorekeeper import EightballGame, NineballGame, PlayerStats
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

    @property
    def player1_name(self):
        return self.player1.name

    @property
    def player2_name(self):
        return self.player2.name

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    lags_won = db.Column(db.Integer, default=0)
    eightball_stats = db.relationship('EightballStats', backref='player', lazy=True)
    nineball_stats = db.relationship('NineballStats', backref='player', lazy=True)

class EightballStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    skill_level = db.Column(db.Integer)
    match_sn_history = db.Column(db.Text)
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
    match_sn_history = db.Column(db.Text)
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
            response = make_response('', 303)  # 303 See Other is recommended for POST-redirect-GET pattern
            response.headers['HX-Redirect'] = url_for('home')
            return response
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        existing_user = Player.query.filter_by(name=name).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Player(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/')
def home():
    if 'user_id' in session:
        players = Player.query.with_entities(Player.id, Player.name).all()
        player_data = [{'id': player.id, 'name': player.name} for player in players]
    else:
        return redirect(url_for('login'))
    
    return render_template('index.html', players=player_data)
@app.route('/game/start', methods=['POST'])
def start_game():
    player1_id = request.form.get('player1_id')
    player2_id = request.form.get('player2_id')
    game_type = request.form.get('game_type')

    if not player1_id or not player2_id or player1_id == player2_id or game_type not in ['8ball', '9ball']:
        return jsonify({'error': 'Invalid request'}), 400

    player1 = Player.query.get(player1_id)
    player2 = Player.query.get(player2_id)
    if not player1 or not player2:
        return jsonify({'error': 'Player not found'}), 404

    existing_game = GameState.query.filter(
        ((GameState.player1_id == player1_id) & (GameState.player2_id == player2_id)) |
        ((GameState.player1_id == player2_id) & (GameState.player2_id == player1_id)),
        GameState.status == 'in_progress',
        GameState.game_type == game_type
    ).first()

    if existing_game:
        return jsonify({'error': 'A game between these players is already in progress'}), 400

    if game_type == '8ball':
        game = EightballGame(player1_name=player1.name, player2_name=player2.name)
    else:
        game = NineballGame(player1_name=player1.name, player2_name=player2.name)

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

    return render_template('partials/game_started.html', game_type=game_type.title(), game_id=new_game_state.id), 201

@app.route('/game/stats/<int:game_id>', methods=['GET'])
def game_stats(game_id):
    game_state = GameState.query.get(game_id)

    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    user_id = session.get('user_id')
    if game_state.player1_id != user_id and game_state.player2_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    game_state_dict = json.loads(game_state.current_state)

    return jsonify(game_state_dict)

@app.route('/current_matches')
def current_matches():
    if 'user_id' not in session:
        return 'You must be logged in to view matches', 403
    user_id = session['user_id']
    matches = GameState.query.filter(
        (GameState.player1_id == user_id) | (GameState.player2_id == user_id),
        GameState.status == 'in_progress'
    ).all()
    
    options_html = '<select id="current_match_select" class="border rounded px-2 py-1">'
    options_html += '<option value="" selected disabled>Select a match</option>'
    for match in matches:
        options_html += f'<option value="{match.id}">{match.player1.name} vs {match.player2.name} - {match.game_type.capitalize()}</option>'
    options_html += '</select>'
    return options_html
@app.route('/get_players/<int:match_id>')
def get_players(match_id):
    game_state = GameState.query.get(match_id)

    if not game_state:
        return jsonify({'error': 'Match not found'}), 404

    players = {
        'player1_name': game_state.player1_name,
        'player2_name': game_state.player2_name
    }

    return jsonify(players)

@app.route('/game_action_form/<int:match_id>')
def game_action_form(match_id):
    game_state = GameState.query.get_or_404(match_id)
    form_template = f"{game_state.game_type}_form.html"
    return render_template(form_template, match_id=match_id)
@app.route('/game/action', methods=['POST'])
def game_action():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401

        match_id = request.form.get('match_id')
        action = request.form.get('action')
        ball_number = request.form.get('ball_number')
        lag_winner = request.form.get('lag_winner')

        logging.debug(f"Received action: {action}, match_id: {match_id}, ball_number: {ball_number}, lag_winner: {lag_winner}")

        game_state_record = GameState.query.filter_by(id=match_id).first()
        if not game_state_record:
            return jsonify({'error': 'Match not found'}), 404

        game_type = game_state_record.game_type
        current_state = json.loads(game_state_record.current_state)

        if action not in ['lag_to_break', 'take_break_shot', 'pocket_ball', 'switch_turn', 'end_game']:
            return jsonify({'error': 'Invalid action'}), 400

        if game_type == '8ball':
            valid_keys = ['current_turn', 'balls_remaining']  # Only include keys not explicitly passed
            filtered_state = {k: v for k, v in current_state.items() if k in valid_keys}
            current_game = EightballGame(
                player1_name=game_state_record.player1_name,
                player2_name=game_state_record.player2_name,
                **filtered_state
            )
        elif game_type == '9ball':
            valid_keys = ['rack_state', 'current_turn']  # Only include keys not explicitly passed
            filtered_state = {k: v for k, v in current_state.items() if k in valid_keys}
            current_game = NineballGame(
                player1_name=game_state_record.player1_name,
                player2_name=game_state_record.player2_name,
                **filtered_state
            )
        else:
            return jsonify({'error': 'Invalid game type'}), 400

        try:
            if action == 'lag_to_break':
                current_game.lag_for_the_break(lag_winner)
            elif action == 'take_break_shot':
                current_game.take_break_shot(ball_pocketed=ball_number)
            elif action == 'pocket_ball' and ball_number is not None:
                try:
                    ball_number = int(ball_number)
                except ValueError:
                    return jsonify({'error': 'Invalid ball number'}), 400
                valid_ball = (1 <= ball_number <= 15 if game_type == '8ball' else 1 <= ball_number <= 9)
                if not valid_ball:
                    return jsonify({'error': 'Invalid ball number for the game type'}), 400
                current_game.pocket_ball(ball_number)
            elif action == 'switch_turn':
                current_game.switch_turn()
            elif action == 'end_game':
                current_game.end_game()

            game_state_record.current_state = json.dumps(current_game.__dict__)
            db.session.commit()

            return jsonify({
                'message': 'Action processed successfully',
                'current_game_state': current_game.__dict__
            })
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error processing action: {str(e)}")
            return jsonify({'error': 'Failed to process action', 'details': str(e)}), 500
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
