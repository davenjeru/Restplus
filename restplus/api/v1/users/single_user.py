from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import safe_user_output, check_id_availability
from restplus.models import users_list

users_ns = Namespace('users')


class SingleUser(Resource):
    def get(self, user_id):
        return dict(user=safe_user_output(self, check_id_availability(self, user_id, users_list, 'user')))

    def patch(self, user_id):
        pass

    def delete(self, user_id):
        pass
