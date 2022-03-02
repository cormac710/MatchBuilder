from src.utilities.environment_variables import ROOT_PORT
from flask import Flask
from flask_cors import CORS

from src.api.create_tables import create_tables
from src.api.register_routes import register_routes

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'} })

create_tables()
register_routes(app)

print(f'Starting at port {ROOT_PORT}')
app.run(port=ROOT_PORT)
