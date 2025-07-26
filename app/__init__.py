from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Importar blueprints
    from .routes.messages import messages_bp
    from .routes.users import users_bp
    from .routes.comments import comments_bp 
    from .routes.auth import auth_bp

    # Registrar blueprints
    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(comments_bp, url_prefix="/comments")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from .models.user import User
    from .models.message import Message
    from .models.comment import Comment

    register_error_handlers(app)

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