from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import safe_user_output
from restplus.models import users_list

users_ns = Namespace('users')


class SingleUser(Resource):
    def get(self, user_id):
        for user in users_list:
            if user.id == user_id:
                return dict(user=safe_user_output(self, user))
        else:
            users_ns.abort(400, 'user not found!')

    def patch(self, user_id):
        pass

    def delete(self, user_id):
        pass
