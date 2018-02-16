from flask import redirect
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import check_id_availability
from restplus.api.v1.posts.single_post import SinglePost
from restplus.models import users_list

users_ns = Namespace('users')


class SingleUserSinglePost(Resource):
    def get(self, user_id, post_id):
        check_id_availability(self, user_id, users_list, 'user')
        return redirect(self.api.url_for(SinglePost, post_id=post_id))

    def put(self, user_id, post_id):
        pass

    def delete(self, user_id, post_id):
        pass
