from flask import url_for

from restplus.models import password_pattern, email_pattern


def extract_auth_data(namespace, where_from):
    """

    :param namespace: The namespace that owns the resource that calls this function
    :param where_from: The url where this fuction is called from
    :return: email and password if called from 'auth_login'
            (and confirm_password if called from 'auth_register')
    :rtype: tuple
    """
    api = namespace.apis[0]
    if not api.payload:
        namespace.abort(415, 'request data not in json format')

    payload = api.payload
    email = payload.get('email')
    password = payload.get('password')
    confirm_password = payload.get('confirm_password')

    if not email:
        namespace.abort(400, 'missing \'email\' parameter')

    if not bool(email_pattern.match(email)):
        namespace.abort(400, 'email address syntax is invalid')

    if not password:
        namespace.abort(400, 'missing \'password\' parameter')

    if not bool(password_pattern.match(password)):
        namespace.abort(400, 'password syntax is invalid')

    if where_from == url_for(api.endpoint('auth_login')):
        return email, password
    elif where_from == url_for(api.endpoint('auth_register')):
        if not confirm_password:
            namespace.abort(400, 'missing \'confirm_password\' parameter')

        if password != confirm_password:
            namespace.abort(400, 'passwords do not match')

        return email, password, confirm_password
