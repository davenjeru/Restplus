from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import check_id_availability, safe_post_output
from restplus.models import users_list, posts_list

users_ns = Namespace('users')


class SingleUserSinglePost(Resource):
    def get(self, user_id, post_id):
        check_id_availability(self, user_id, users_list, 'user')

        a_post = check_id_availability(self, post_id, posts_list, 'post')

        return dict(post=safe_post_output(self, a_post))

    def put(self, user_id, post_id):
        pass

    def delete(self, user_id, post_id):
        pass
