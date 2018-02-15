from flask_restplus import Resource
from flask_restplus.namespace import Namespace

posts_ns = Namespace('posts')


class AllPosts(Resource):
    def get(self):
        pass
