from restplus.api.v1.helpers import validate, get_namespace, json_checker, safe_post_output


def extract_post_data(resource):
    api = resource.api
    namespace = get_namespace(api, resource)
    json_checker(api, namespace)

    payload = api.payload
    title = payload.get('title')
    validate('title', title, namespace)

    body = payload.get('body')
    validate('body', body, namespace)

    return title.title(), body


def generate_post_output(resource, post, method):
    output_dict = dict(post=safe_post_output(resource, post))

    if resource.endpoint == 'users_single_user_all_posts':
        if method == 'post':
            output_dict['message'] = 'post created successfully'

    return output_dict
