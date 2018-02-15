from flask_login import current_user, logout_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.auth.helpers import generate_auth_output

auth_ns = Namespace('auth')


class Logout(Resource):
    @auth_ns.response(200, 'user logged out successfully')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User Logout

        Makes use of Flask-Login

        """
        try:
            output = generate_auth_output(self, current_user)
            logout_user()
            return self.api.make_response(output, 200)
        except AttributeError:
            logout_user()
            auth_ns.abort(400, 'no user in session')
