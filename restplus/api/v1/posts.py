from flask_restplus import Resource
from flask_restplus.namespace import Namespace

posts_ns = Namespace('posts', description='Operations on posts only')


@posts_ns.route('/')
class AllPosts(Resource):
    def get(self):
        pass


@posts_ns.route('/<int:post_id>')
class Login(Resource):
    def get(self, post_id):
        pass
