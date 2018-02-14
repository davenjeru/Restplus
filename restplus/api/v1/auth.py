from flask import url_for
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from restplus.models import User, users_list, password_pattern, email_pattern

auth_ns = Namespace('auth', description='Operations related to authentication')


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(auth_ns.model('user_register',
                                  {
                                      'email': fields.String(title='Your email address', required=True,
                                                             example='myemail@company.com'),
                                      'password': fields.String(title='Your email address', required=True,
                                                                example='password.Pa55word'),
                                      'confirm_password': fields.String(title='Your email address', required=True,
                                                                        example='password.Pa55word')
                                  }))
    @auth_ns.response(201, 'user created successfully')
    @auth_ns.response(415, 'request data not in json format')
    def post(self):
        """
        User registration

        1. Email address should be syntactically valid.
        2. Password should have a minimum of 12 characters and a maximum of 80 characters
        3. Password should have no spaces
        4. Password should have at least one number, uppercase and lowercase letter.
        5. Password should have at least one of these special characters !@#$%^;*()_+}{:'?/.,

        """
        this_api = auth_ns.apis[0]
        if not this_api.payload:
            auth_ns.abort(415, 'request data not in json format')

        payload = this_api.payload
        email = payload.get('email')
        password = payload.get('password')
        confirm_password = payload.get('confirm_password')

        if not email or not password or not confirm_password:
            auth_ns.abort(400, 'missing one or more parameters')

        if not bool(email_pattern.match(email)):
            auth_ns.abort(400, 'email address syntax is invalid')

        for a_user in users_list:
            if email == a_user.email:
                auth_ns.abort(400, 'user with same email address exists!')

        if not bool(password_pattern.match(password)):
            auth_ns.abort(400, 'password syntax is invalid')

        if password != confirm_password:
            auth_ns.abort(400, 'passwords do not match')

        created_user = User(email, password)
        created_user.save()

        output = {
            'user': {'email': created_user.email,
                     'url': url_for(this_api.endpoint('users_single_user'), user_id=created_user.id)},
            'message': 'user created successfully'}

        response = this_api.make_response(output, 201)
        response.headers['location'] = url_for(this_api.endpoint('users_single_user'), user_id=created_user.id)

        return response


@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        pass


@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        pass
