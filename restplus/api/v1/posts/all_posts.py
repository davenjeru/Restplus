from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import safe_post_output
from restplus.models import posts_list

posts_ns = Namespace('posts')


class AllPosts(Resource):
    def get(self):
        """
        View all posts
        :return: a list of all posts under 'posts'

        :rtype dict

        """
        posts = []
        for post in posts_list:
            posts.append(safe_post_output(self, post))
        return dict(posts=posts)
