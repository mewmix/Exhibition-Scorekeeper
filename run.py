from app import create_app, db
from app.models.models import User, Game  # Adjust imports based on your 
models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game}  # Adjust based on your 
models
