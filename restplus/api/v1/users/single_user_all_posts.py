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

    def get(self, user_id: int):
        check_id_availability(self, user_id, users_list, str(User.__name__))
        my_posts_list, my_posts_list_output = self.my_posts(user_id)
        return dict(posts=my_posts_list_output)

    @users_ns.expect(post_model)
    @login_required
    def post(self, user_id: int):
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
    def delete(self, user_id: int):
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
