from flask import url_for
from flask_login import current_user, logout_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

auth_ns = Namespace('auth')


class Logout(Resource):
    @auth_ns.response(200, 'user logged out successfully')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User Logout

        Makes use of Flask-Login

        """
        api = self.api
        try:
            output = {
                'user': {'email': current_user.email,
                         'url': url_for(api.endpoint('users_single_user'), user_id=current_user.id)},
                'message': 'user logged out successfully'}
            logout_user()
            return api.make_response(output, 200)
        except AttributeError:
            logout_user()
            auth_ns.abort(400, 'no user in session')
