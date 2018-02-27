from flask import redirect
from flask_login import login_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import check_id_availability
from restplus.api.v1.posts.single_post import SinglePost
from restplus.api.v1.users.helpers import extract_post_data, patch_post, generate_post_output
from restplus.api.v1.users.single_user_all_posts import post_model
from restplus.models import users_list, posts_list, Post, User

users_ns = Namespace('users')


class SingleUserSinglePost(Resource):
    def get(self, user_id: int, post_id: int):
        """
        View a single post from a specific user
        """
        check_id_availability(self, user_id, users_list, str(User.__name__))
        check_id_availability(self, post_id, posts_list, str(Post.__name__))
        for post in posts_list:
            if post.user_id == user_id and post.id == post_id:
                return redirect(self.api.url_for(SinglePost, post_id=post_id))
        else:
            users_ns.abort(400, 'the requested user does not own this post')

    @login_required
    @users_ns.expect(post_model)
    @users_ns.response(200, 'Post modified successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def patch(self, user_id: int, post_id: int):
        """
        Modify a post

        1. User should be logged in.
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created
        """
        check_id_availability(self, user_id, users_list, str(User.__name__))
        this_post = check_id_availability(self, post_id, posts_list, str(Post.__name__))

        if current_user.id != user_id:
            users_ns.abort(403)

        for post in posts_list:
            if post.user_id == user_id and post.id == post_id:
                this_post = post
                break
        else:
            users_ns.abort(400, 'the requested user does not own this post')

        title, body = extract_post_data(self, str(self.patch.__name__))

        for post in posts_list:
            if post.title == title and post.body == body:
                users_ns.abort(400, 'a similar post exists')

            if body and body == post.body:
                users_ns.abort(400, 'a similar post exists')

        if title:
            this_post = patch_post(self, ('title', title,), current_user, this_post)
        if body:
            this_post = patch_post(self, ('body', body,), current_user, this_post)

        response = self.api.make_response(generate_post_output(self, this_post, str(self.patch.__name__)), 200)
        response.headers['location'] = self.api.url_for(SingleUserSinglePost, user_id=user_id, post_id=post_id)

        return response

    @login_required
    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int, post_id: int):
        """
        Delete a post

        1. User needs to be logged in
        2. This deletes the post whose ID is specified on the url
        3. This process is irreversible
        """
        check_id_availability(self, user_id, users_list, str(User.__name__))
        this_post = check_id_availability(self, post_id, posts_list, str(Post.__name__))

        if current_user.id != user_id:
            users_ns.abort(403)

        for post in posts_list:
            if post.user_id == user_id and post.id == post_id:
                this_post = post
                break
        else:
            users_ns.abort(400, 'the requested user does not own this post')

        try:
            current_user.delete_post(this_post)
        except AssertionError as a:
            users_ns.abort(400, a.args[0])

        response = self.api.make_response(None, 204)
        return response
