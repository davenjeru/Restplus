from flask import Blueprint
from flask_restplus import Api

api_v1_blueprint = Blueprint('apiV1', __name__, url_prefix='/api/v1')
api_v1 = Api(api_v1_blueprint)
