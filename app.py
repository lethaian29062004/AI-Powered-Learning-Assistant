from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Import and register blueprint
    from routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app

app = create_app() 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
