from flask_restplus import Resource
from flask_restplus.namespace import Namespace

posts_ns = Namespace('posts')


class SinglePost(Resource):
    def get(self, post_id):
        pass
