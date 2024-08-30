from flask import Blueprint, request, session, jsonify, render_template, url_for, redirect, make_response
from app import db, bcrypt
from app.models import Player

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = Player.query.filter_by(name=name).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            response = make_response('', 303)  # 303 See Other is recommended for POST-redirect-GET pattern
            response.headers['HX-Redirect'] = url_for('auth.home')  # Updated
            return response
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
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

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.home'))  # Updated

@auth_bp.route('/')
def home():
    if 'user_id' in session:
        players = Player.query.with_entities(Player.id, Player.name).all()
        player_data = [{'id': player.id, 'name': player.name} for player in players]
    else:
        return redirect(url_for('auth.login'))  # Updated
    
    return render_template('index.html', players=player_data)
