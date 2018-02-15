from flask_restplus.namespace import Namespace

from restplus.api.v1.auth.login import Login, user_login_model
from restplus.api.v1.auth.logout import Logout
from restplus.api.v1.auth.register import Register, user_register_model

auth_ns = Namespace('auth', description='Operations related to authentication')

auth_ns.add_resource(Register, '/register', endpoint='auth_register')
auth_ns.add_model('user_register', user_register_model)

auth_ns.add_resource(Login, '/login')
auth_ns.add_model('user_login', user_login_model)

auth_ns.add_resource(Logout, '/logout')
