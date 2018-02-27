from flask import url_for
from flask_login import current_user, login_required
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import check_id_availability
from restplus.api.v1.users.helpers import extract_post_data, generate_post_output, safe_post_output
from restplus.models import users_list, posts_list, User

users_ns = Namespace('users')
post_model = users_ns.model('post_model', {
    'title': fields.String(title='The title of your post', required=True,
                           example='My Post Title'),
    'body': fields.String(title='The body of your post', required=True,
                          example='Something interesting for people to read.')
})


class SingleUserAllPosts(Resource):

    def my_posts(self, user_id: int):
        my_posts_list = []
        my_posts_list_output = []
        for a_post in posts_list:
            if a_post.user_id == user_id:
                post_dict = safe_post_output(self, a_post)
                post_dict.pop('author_url')
                my_posts_list_output.append(post_dict)
                my_posts_list.append(a_post)
        return my_posts_list, my_posts_list_output

    @users_ns.response(200, "Success")
    @users_ns.response(400, "Post not found. Invalid 'post_id' provided")
    def get(self, user_id: int):
        """
        View all posts from a single user
        """
        check_id_availability(self, user_id, users_list, str(User.__name__))
        my_posts_list, my_posts_list_output = self.my_posts(user_id)
        return dict(posts=my_posts_list_output)

    @users_ns.expect(post_model)
    @login_required
    @users_ns.response(201, 'Post created successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Add a post

        1. User must be logged in to create a post
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created

        """
        check_id_availability(self, user_id, users_list, str(User.__name__))

        if current_user.id != user_id:
            users_ns.abort(403)

        title, body = extract_post_data(self, str(self.post.__name__))
        for a_post in posts_list:
            if a_post.title == title and a_post.body == body:
                users_ns.abort(400, 'post already exists')

        post = current_user.create_post(title, body)
        output = generate_post_output(self, post, 'post')
        response = self.api.make_response(output, 201)
        response.headers['location'] = url_for(self.api.endpoint('users_single_user_single_post'),
                                               user_id=post.user_id, post_id=post.id)
        return response

    @login_required
    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int):
        """
        Batch delete all user's posts

        1. User must be logged in to delete all their posts
        2. This deletes all posts that a user has created
        3. This process os of course irreversible
        """
        check_id_availability(self, user_id, users_list, str(User.__name__))

        if current_user.id != user_id:
            users_ns.abort(403)

        my_posts_list, my_posts_list_output = self.my_posts(user_id)

        for a_post in my_posts_list:
            try:
                current_user.delete_post(a_post)
            except AssertionError as a:
                users_ns.abort(400, a.args[0])

        return None, 204
