from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from .routes import  errors_scope
from .routes.api.user import api_user
from .routes.api.events import api_events
from .routes.api.tickets import api_tickets

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)
app.register_blueprint(errors_scope, url_prefix="/")
app.register_blueprint(api_user, url_prefix="/api/user")
app.register_blueprint(api_events, url_prefix="/api/events")
app.register_blueprint(api_tickets, url_prefix="/api/tickets")

# @app.errorhandler(500)
# def handle_internal_server_error(e):
#     return jsonify(error=e.description), 500, {"Content-Type": "application/json"}
# reset_table()
