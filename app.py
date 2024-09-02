from flask import Flask, request, session, jsonify, render_template, url_for, redirect, make_response
from flask_cors import CORS
import json
import time
from scrimage_scorekeeper import NineballGame
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
from flask import Flask, request, session, jsonify, render_template, url_for, redirect, make_response
from flask_cors import CORS
import json
import time
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # For password hashing
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scorekeeper.db'
app.config['SECRET_KEY'] = 'MOOOCOWMOOOOOO'

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)
bcrypt = Bcrypt(app)

# Database models
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
class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    game_type = db.Column(db.String(50))  # '8ball' or '9ball'
    status = db.Column(db.String(50), default='in_progress')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    break_shot_taken = db.Column(db.Boolean, default=False)
    # Game state specific fields
    current_shooter = db.Column(db.String(80))
    inning_total = db.Column(db.Integer)
    lag_winner = db.Column(db.String(80))
    eightball_rack_count = db.Column(db.Integer)
    match_winner = db.Column(db.String(80))
    player1_balls_pocketed = db.Column(db.Text)  # Comma-separated ball numbers
    player2_balls_pocketed = db.Column(db.Text)
    game_log = db.Column(db.Text)  # Serialized as a string with newlines

    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])

    @property
    def player1_name(self):
        return self.player1.name

    @property
    def player2_name(self):
        return self.player2.name

    def get_player1_balls(self):
        return self.player1_balls_pocketed.split(',') if self.player1_balls_pocketed else []

    def get_player2_balls(self):
        return self.player2_balls_pocketed.split(',') if self.player2_balls_pocketed else []

    def update_player1_balls(self, balls):
        self.player1_balls_pocketed = ','.join(balls)

    def update_player2_balls(self, balls):
        self.player2_balls_pocketed = ','.join(balls)

    def get_game_log(self):
        return self.game_log.split('\n') if self.game_log else []

    def add_to_game_log(self, log_entry):
        if self.game_log:
            self.game_log += f'\n{log_entry}'
        else:
            self.game_log = log_entry

class EightballGame:
    def __init__(self, game_state):
        self.game_state = game_state

    def lag_for_the_break(self, lag_winner):
        if lag_winner not in [self.game_state.player1_name, self.game_state.player2_name]:
            raise ValueError('Invalid lag winner')

        self.game_state.lag_winner = lag_winner
        self.game_state.rack_breaking_player = lag_winner
        self.game_state.current_shooter = lag_winner
        self.game_state.add_to_game_log(f'{lag_winner} wins the lag and will break')


    def take_break_shot(self, ball_pocketed=None):
        # Check if the break shot has already been taken
        if self.game_state.break_shot_taken:
            raise ValueError('Break shot already taken')

        # Mark the break shot as taken
        self.game_state.break_shot_taken = True
        self.game_state.add_to_game_log(f'{self.game_state.current_shooter} takes the break shot')

        # Handle the case where ball_pocketed is an empty string or None
        if ball_pocketed and ball_pocketed.strip() != '':
            try:
                ball_pocketed = int(ball_pocketed)
            except ValueError:
                raise ValueError('Invalid ball number')

            if ball_pocketed == 8:
                self.game_state.match_winner = self.game_state.current_shooter
                self.game_state.add_to_game_log(f'{self.game_state.current_shooter} wins the game by pocketing the 8-ball on the break')
            elif ball_pocketed == 0:
                opponent = self.game_state.player1_name if self.game_state.current_shooter == self.game_state.player2_name else self.game_state.player2_name
                self.game_state.match_winner = opponent
                self.game_state.add_to_game_log(f'{self.game_state.current_shooter} scratches on the break. {opponent} wins the game')
            else:
                self.game_state.add_to_game_log(f'{self.game_state.current_shooter} pockets ball {ball_pocketed} on the break')
        else:
            # No ball was pocketed on the break
            self.game_state.add_to_game_log(f'No balls pocketed on the break. Turn switches to {self.game_state.current_shooter}')
            self.switch_turn()

        if self.is_game_over():
            self.end_game()

    def pocket_ball(self, ball_number):

        if self.game_state.current_shooter == self.game_state.player1_name:
            pocketed_balls = self.game_state.get_player1_balls()
            pocketed_balls.append(str(ball_number))
            self.game_state.update_player1_balls(pocketed_balls)
        else:
            pocketed_balls = self.game_state.get_player2_balls()
            pocketed_balls.append(str(ball_number))
            self.game_state.update_player2_balls(pocketed_balls)

        self.game_state.add_to_game_log(f'Player {self.game_state.current_shooter} pocketed ball {ball_number}')

        if self.is_game_over():
            self.end_game()

    def switch_turn(self):
        if self.game_state.current_shooter == self.game_state.player1_name:
            self.game_state.current_shooter = self.game_state.player2_name
        else:
            self.game_state.current_shooter = self.game_state.player1_name

    def is_game_over(self):
        return bool(self.game_state.match_winner)

    def end_game(self):
        self.game_state.match_end_timestamp = time.time()
        self.game_state.add_to_game_log(f'Player {self.game_state.current_shooter} wins the game')

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

    new_game_state = GameState(
        player1_id=player1_id,
        player2_id=player2_id,
        game_type=game_type,
        current_shooter=player1.name if game_type == '8ball' else None,
        inning_total=0,
        lag_winner=None,
        eightball_rack_count=1,
        match_winner=None,
        player1_balls_pocketed="",
        player2_balls_pocketed="",
        game_log=""
    )
    db.session.add(new_game_state)
    db.session.commit()

    if game_type == '8ball':
        game = EightballGame(new_game_state)
    else:
        game = NineballGame(new_game_state)

    return render_template('partials/game_started.html', game_type=game_type.title(), game_id=new_game_state.id), 201
@app.route('/game/stats/<int:game_id>', methods=['GET'])
def game_stats(game_id):
    game_state = db.session.get(GameState, game_id)  # Updated to SQLAlchemy 2.0

    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    user_id = session.get('user_id')
    if game_state.player1_id != user_id and game_state.player2_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    # Create a dictionary representing the current game state
    game_state_dict = {
        "player1_name": game_state.player1_name,
        "player2_name": game_state.player2_name,
        "current_shooter": game_state.current_shooter,
        "inning_total": game_state.inning_total,
        "lag_winner": game_state.lag_winner,
        "eightball_rack_count": game_state.eightball_rack_count,
        "match_winner": game_state.match_winner,
        "player1_balls_pocketed": game_state.get_player1_balls(),
        "player2_balls_pocketed": game_state.get_player2_balls(),
        "game_log": game_state.get_game_log()
    }

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

        logging.debug(f"Received action: {action}, match_id: {match_id}, ball_number: {ball_number}")

        game_state_record = db.session.get(GameState, match_id)  # Fetch the game state
        if not game_state_record:
            return jsonify({'error': 'Match not found'}), 404

        game_type = game_state_record.game_type

        if game_type == '8ball':
            current_game = EightballGame(game_state_record)
        elif game_type == '9ball':
            current_game = NineballGame(game_state_record)
        else:
            return jsonify({'error': 'Invalid game type'}), 400

        try:
            if action == 'pocket_ball' and ball_number:
                try:
                    ball_number = int(ball_number)
                    current_game.pocket_ball(ball_number)
                except ValueError:
                    return jsonify({'error': 'Invalid ball number'}), 400

            # After processing the action, commit the updated game state to the database
            db.session.commit()

            return jsonify({
                'message': 'Action processed successfully',
                'current_game_state': {
                    "player1_balls_pocketed": game_state_record.get_player1_balls(),
                    "player2_balls_pocketed": game_state_record.get_player2_balls(),
                    "game_log": game_state_record.get_game_log()
                }
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
