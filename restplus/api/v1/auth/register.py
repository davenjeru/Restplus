from flask import url_for
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from restplus.api.v1.auth.helpers import extract_auth_data
from restplus.models import User, users_list

auth_ns = Namespace('auth')

user_register_model = auth_ns.model('user_register', {
    'email': fields.String(title='Your email address', required=True,
                           example='myemail@company.com'),
    'password': fields.String(title='Your email address', required=True,
                              example='password.Pa55word'),
    'confirm_password': fields.String(title='Your email address', required=True,
                                      example='password.Pa55word')
})


class Register(Resource):
    @auth_ns.expect(user_register_model)
    @auth_ns.response(201, 'user created successfully')
    @auth_ns.response(415, 'request data not in json format')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User registration

        1. Email address should be syntactically valid.
        2. Password should have a minimum of 12 characters and a maximum of 80 characters
        3. Password should have no spaces
        4. Password should have at least one number, uppercase and lowercase letter.
        5. Password should have at least one of these special characters !@#$%^;*()_+}{:'?/.,

        """
        api = self.api
        namespace = None
        for a_namespace in api.namespaces:
            if a_namespace.path in api.url_for(self):
                namespace = a_namespace
                break

        email, password, confirm_password = extract_auth_data(namespace, api.url_for(self))

        for a_user in users_list:
            if email == a_user.email:
                auth_ns.abort(400, 'user with same email address exists!')

        created_user = User(email, password)
        created_user.save()

        output = {
            'user': {'email': created_user.email,
                     'url': url_for(api.endpoint('users_single_user'), user_id=created_user.id)},
            'message': 'user created successfully'}

        response = api.make_response(output, 201)
        response.headers['location'] = url_for(api.endpoint('users_single_user'), user_id=created_user.id)

        return response
