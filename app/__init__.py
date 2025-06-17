from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import Config
import os

db = SQLAlchemy()

ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Caminho do arquivo .db
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes.messages import messages_bp
    from .routes.users import users_bp

    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.register_blueprint(users_bp, url_prefix="/users")

    from .schemas.user_schema import UserSchema
    users_schema = UserSchema(many=True)

    from .models.message import Message
    from .models.user import User

    @app.route("/hello")
    def hello():
        users = User.query.all()
        users_json = [user.to_dict() for user in users]
        return jsonify(users_json)
    register_error_handlers(app)

    # Criação do banco de dados
    with app.app_context():
        db.create_all()
        print('Banco de dados criado com sucesso!')

    return app

from flask import jsonify

        
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500
