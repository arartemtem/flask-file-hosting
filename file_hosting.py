from app import app, db
from app.models import User, File, FilePath

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'File': File, 'FilePath': FilePath}
