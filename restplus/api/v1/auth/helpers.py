from flask import url_for

from restplus.api.v1.helpers import safe_user_output
from restplus.models import password_pattern, email_pattern


def extract_auth_data(resource):
    """

    :param resource: The resource that called this function
    :return: email and password if called from 'auth_login'
            (and confirm_password if called from 'auth_register')
    :rtype: tuple
    """
    api = resource.api
    namespace = get_auth_namespace(api, resource)
    if not api.payload:
        namespace.abort(415, 'request data not in json format')

    payload = api.payload
    email = payload.get('email')
    validate('email', email, namespace)

    password = payload.get('password')
    validate('password', password, namespace)

    if api.url_for(resource) == url_for(api.endpoint('auth_login')):
        return email, password
    elif api.url_for(resource) == url_for(api.endpoint('auth_register')):
        confirm_password = payload.get('confirm_password')
        validate('confirm_password', confirm_password, namespace)

        if password != confirm_password:
            namespace.abort(400, 'passwords do not match')

        return email, password, confirm_password


def generate_auth_output(resource, user):
    api = resource.api
    output_dict = dict(user=safe_user_output(resource, user))

    if api.url_for(resource) == url_for(api.endpoint('auth_register')):
        output_dict['message'] = 'user registered successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_login')):
        output_dict['message'] = 'user logged in successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_logout')):
        output_dict['message'] = 'user logged out successfully'

    return output_dict


def get_auth_namespace(api, resource):
    for a_namespace in api.namespaces:
        # default namespace has '' as path
        # the if statement below takes care of this
        if a_namespace.path and a_namespace.path in api.url_for(resource):
            return a_namespace


def validate(name, item, namespace):
    if not item:
        namespace.abort(400, 'missing \"{0}\" parameter'.format(name))

    if name == 'email':
        if not bool(email_pattern.match(item)):
            namespace.abort(400, 'email address syntax is invalid')
    elif name == 'password':
        if not bool(password_pattern.match(item)):
            namespace.abort(400, 'password syntax is invalid')
    elif name == 'confirm_password':
        if not bool(password_pattern.match(item)):
            namespace.abort(400, 'please confirm password using the password syntax guidelines provided')
