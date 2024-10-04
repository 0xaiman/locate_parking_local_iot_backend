from flask import Flask, request, jsonify
from config.db_connect import create_connection
from routes.routes import setup_routes
app = Flask(__name__)

create_connection()

setup_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
