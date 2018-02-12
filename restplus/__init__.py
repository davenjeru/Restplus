from flask import Flask
from restplus.api.v1 import api_v1_blueprint

# initiate app
app = Flask(__name__)

# register blueprints
app.register_blueprint(api_v1_blueprint)