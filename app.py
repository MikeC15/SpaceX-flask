from flask import Flask, jsonify, g
from flask_cors import CORS
from resources.users import user
from resources.comments import comment
from flask_login import LoginManager
import models


DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'asdfghjkl'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')
CORS(comment, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(comment, url_prefix='/api/v1/comments')

# @app.route('/')
# def index():
#     return 'hii'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)