from app import app, db
from app.models import User, File, FilePath

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'File': File, 'FilePath': FilePath}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
