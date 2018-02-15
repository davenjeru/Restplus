from flask import url_for

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
    validate_email(email, namespace)

    password = payload.get('password')
    confirm_password = payload.get('confirm_password')
    validate_password(password, namespace)

    if api.url_for(resource) == url_for(api.endpoint('auth_login')):
        return email, password
    elif api.url_for(resource) == url_for(api.endpoint('auth_register')):
        if not confirm_password:
            namespace.abort(400, 'missing \'confirm_password\' parameter')

        if password != confirm_password:
            namespace.abort(400, 'passwords do not match')

        return email, password, confirm_password


def generate_auth_output(resource, user):
    api = resource.api
    output_dict = {
        'user': {'email': user.email,
                 'url': url_for(api.endpoint('users_single_user'), user_id=user.id)}}

    if api.url_for(resource) == url_for(api.endpoint('auth_register')):
        output_dict['message'] = 'user logged in successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_login')):
        output_dict['message'] = 'user logged in successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_logout')):
        output_dict['message'] = 'user logged in successfully'

    return output_dict


def get_auth_namespace(api, resource):
    for a_namespace in api.namespaces:
        # default namespace has '' as path
        # the if statement below takes care of this
        if a_namespace.path and a_namespace.path in api.url_for(resource):
            return a_namespace


def validate_email(email, namespace):
    if not email:
        namespace.abort(400, 'missing \'email\' parameter')

    if not bool(email_pattern.match(email)):
        namespace.abort(400, 'email address syntax is invalid')


def validate_password(password, namespace):
    if not password:
        namespace.abort(400, 'missing \'password\' parameter')

    if not bool(password_pattern.match(password)):
        namespace.abort(400, 'password syntax is invalid')
