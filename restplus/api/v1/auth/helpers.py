from flask import url_for

from restplus.api.v1.helpers import safe_user_output, validate, get_namespace, json_checker


def extract_auth_data(resource):
    """

    :param resource: The resource that called this function
    :return: email and password if called from 'auth_login'
            (and confirm_password if called from 'auth_register')
    :rtype: tuple
    """
    api = resource.api
    namespace = get_namespace(api, resource)
    json_checker(api, namespace)

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

