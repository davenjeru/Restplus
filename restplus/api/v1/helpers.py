from flask import url_for


def safe_user_output(resource, user):
    api = resource.api
    user_dict = user.serialize
    user_dict['url'] = url_for(api.endpoint('users_single_user'), user_id=user.id)
    return user_dict
