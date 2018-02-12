from flask_restplus import Resource
from flask_restplus.namespace import Namespace

auth_ns = Namespace('auth', description='Operations related to authentication')


@auth_ns.route('/register')
class Register(Resource):
    def post(self):
        pass


@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        pass


@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        pass
