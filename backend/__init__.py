from flask import Flask, send_from_directory
import os

def create_app():
    # Use an absolute path to the dist directory
    static_folder = '/home/mrnam205/Desktop/BillDischarge/BillDischarge_v2/frontend/dist'
    app = Flask(__name__, static_folder=static_folder)

    with app.app_context():
        # Import and register blueprints
        from .routes import hello
        app.register_blueprint(hello.bp)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app