def load_player_names():
    from app.models import Player  # Import inside the function to avoid circular dependency
    players = Player.query.with_entities(Player.name).all()
    return [player.name for player in players]
