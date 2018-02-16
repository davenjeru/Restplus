import string

from flask import url_for

from restplus.models import email_pattern, password_pattern


def json_checker(api, namespace):
    if not api.payload:
        namespace.abort(415, 'request data not in json format')


def safe_user_output(resource, user):
    api = resource.api
    user_dict = user.serialize
    user_dict['url'] = url_for(api.endpoint('users_single_user'), user_id=user.id)
    return user_dict


def safe_post_output(resource, post):
    api = resource.api
    post_dict = post.serialize
    post_dict['post_url'] = url_for(api.endpoint('users_single_user_single_post'), user_id=post.user_id,
                                    post_id=post.id)
    post_dict['author_url'] = url_for(api.endpoint('users_single_user'), user_id=post.user_id)
    return post_dict


def get_namespace(api, resource):
    for a_namespace in api.namespaces:
        for a_resource in a_namespace.resources:
            if type(resource) in a_resource:
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
    elif name == 'title' or name == 'body':
        validate_title_or_body(name, item, namespace)


def validate_title_or_body(name, item, namespace):
    if name == 'title':
        check_length(name, item, namespace)
    elif name == 'body':
        check_length(name, item, namespace)

    if item[0] not in list(string.ascii_letters) + list(string.digits):
        namespace.abort(400, 'please enter a valid {0}'.format(name))

    if str(item[-1]) not in list(string.ascii_letters) + list(string.digits) + list('\'\").?!'):
        namespace.abort(400, 'please enter a valid {0}'.format(name))

    item_words = item.split(' ')

    unwanted_spaces, item_words = check_for_unwanted_spaces(item_words)

    if not check_subsequent_punctuations(item_words):
        namespace.abort(400, 'please enter a valid {0}'.format(name))

    if not unwanted_spaces:
        suggestion = ' '.join(item_words)
        message = {'error': 'please input a valid {0}'.format(name),
                   'suggestion': 'did you mean "{0}" instead?'.format(suggestion)}
        namespace.abort(400, message)

    return True


def check_subsequent_punctuations(list_of_words):
    for word in list_of_words[:]:
        if word.count('.') > 3:
            return False

        char_list = list(word)
        for i in range(len(char_list) - 1):
            if char_list[i] in string.punctuation and char_list[i] != '.':
                if char_list[i + 1] in string.punctuation and char_list[i] != '.':
                    return False
    else:
        return True


def check_for_unwanted_spaces(list_of_words):
    unwanted_spaces = True
    for word in list_of_words[:]:
        if not word:
            list_of_words.remove(word)
            unwanted_spaces = False

    return unwanted_spaces, list_of_words


def check_length(name, item, namespace):
    if name == 'title':
        if len(item) > 70:
            namespace.abort(400, 'title too long')

        if len(item) < 10:
            namespace.abort(400, 'title too short')
    elif name == 'body':
        if len(item) < 40:
            namespace.abort(400, 'body too short')

        if len(item) > 500:
            namespace.abort(400, 'body too long')


def check_id_availability(resource, the_id, a_list, context):
    api = resource.api
    namespace = get_namespace(api, resource)

    for an_item in a_list:
        if an_item.id == the_id:
            break
    else:
        namespace.abort(400, '{0} not found!'.format(context))
