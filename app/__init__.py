from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import parts of our application
        from .routes import init_routes

        # Initialize routes
        init_routes(app)

    return app
