from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users', description='Operations related to users')


@users_ns.route('/')
class AllUsers(Resource):
    def get(self):
        pass


@users_ns.route('/<int:user_id>')
class SingleUser(Resource):
    def get(self, user_id):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass


@users_ns.route('/<int:user_id>/posts')
class SingleUserAllPosts(Resource):
    def get(self, user_id):
        pass

    def post(self, user_id):
        pass

    def delete(self, user_id):
        pass


@users_ns.route('/<int:user_id>/posts/<int:post_id>')
class SingleUserSinglePost(Resource):
    def get(self, user_id, post_id):
        pass

    def put(self, user_id, post_id):
        pass

    def delete(self, user_id, post_id):
        pass
