from flask import Blueprint, request, session, jsonify, render_template
from app import db
from app.models import Player, GameState
from core.scrimage_scorekeeper import EightballGame, NineballGame
from app.utils.logging_config import setup_logging

# Set up logging
logger = setup_logging(log_file='logs/game.log')

game_bp = Blueprint('game', __name__)


@game_bp.route('/game/start', methods=['POST'])
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

@game_bp.route('/game/stats/<int:game_id>', methods=['GET'])
def game_stats(game_id):
    game_state = GameState.query.get(game_id)

    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    user_id = session.get('user_id')
    if game_state.player1_id != user_id and game_state.player2_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    if game_state.game_type == '8ball':
        player1_stats = EightballStats.query.filter_by(player_id=game_state.player1_id).first()
        player2_stats = EightballStats.query.filter_by(player_id=game_state.player2_id).first()
    elif game_state.game_type == '9ball':
        player1_stats = NineballStats.query.filter_by(player_id=game_state.player1_id).first()
        player2_stats = NineballStats.query.filter_by(player_id=game_state.player2_id).first()
    else:
        return jsonify({'error': 'Invalid game type'}), 400

    game_stats = {
        'player1_name': game_state.player1.name,
        'player2_name': game_state.player2.name,
        'player1_stats': player1_stats,
        'player2_stats': player2_stats
    }

    return render_template('partials/game_stats.html', game_stats=game_stats)


@game_bp.route('/current_matches')
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
@game_bp.route('/get_players/<int:match_id>')
def get_players(match_id):
    game_state = GameState.query.get(match_id)

    if not game_state:
        return jsonify({'error': 'Match not found'}), 404

    players = {
        'player1_name': game_state.player1_name,
        'player2_name': game_state.player2_name
    }

    return jsonify(players)

@game_bp.route('/game_action_form/<int:match_id>')
def game_action_form(match_id):
    game_state = GameState.query.get_or_404(match_id)
    form_template = f"{game_state.game_type}_form.html"
    return render_template(form_template, match_id=match_id)

@game_bp.route('/game/action', methods=['POST'])
def game_action():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401

        match_id = request.form.get('match_id')
        action = request.form.get('action')
        ball_number = request.form.get('ball_number')
        lag_winner = request.form.get('lag_winner')

        logger.debug(f"Received action: {action}, match_id: {match_id}, ball_number: {ball_number}, lag_winner: {lag_winner}")

        game_state_record = GameState.query.filter_by(id=match_id).first()
        if not game_state_record:
            return jsonify({'error': 'Match not found'}), 404

        game_type = game_state_record.game_type
        current_state = json.loads(game_state_record.current_state)

        if action not in ['lag_to_break', 'take_break_shot', 'pocket_ball', 'switch_turn', 'end_game']:
            return jsonify({'error': 'Invalid action'}), 400

        if game_type == '8ball':
            current_game = EightballGame(
                player1_name=game_state_record.player1.name,
                player2_name=game_state_record.player2.name,
                **{k: v for k, v in current_state.items() if k not in ('player1_name', 'player2_name')}
            )
        elif game_type == '9ball':
            current_game = NineballGame(
                player1_name=game_state_record.player1.name,
                player2_name=game_state_record.player2.name,
                **{k: v for k, v in current_state.items() if k not in ('player1_name', 'player2_name')}
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
            logger.error(f"Error processing action: {str(e)}")
            return jsonify({'error': 'Failed to process action', 'details': str(e)}), 500
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

