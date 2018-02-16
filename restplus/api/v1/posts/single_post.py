from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import check_id_availability, safe_post_output
from restplus.models import posts_list

posts_ns = Namespace('posts')


class SinglePost(Resource):
    def get(self, post_id):
        return dict(post=safe_post_output(self, check_id_availability(self, post_id, posts_list, 'post')))
