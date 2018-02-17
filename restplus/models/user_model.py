from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from restplus.models.post_model import Post

users_list = []


class User(UserMixin, object):
    """
    This is the user class.
    Defines a user and all actions that can be done by it.
    """

    id = 1

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = generate_password_hash(password)
        self.id = User.id

    def save(self):
        User.id += 1
        users_list.append(self)

    def get_id(self):
        return chr(self.id)

    def authenticate(self, password: str):
        return check_password_hash(self.password, password)

    @property
    def serialize(self):
        return {'email': self.email}

    @property
    def __name__(self):
        return self.__class__.__name__

    def create_post(self, title: str, body: str):
        my_post = Post(self, title, body)
        my_post.save()
        return my_post

    def update_post(self, name: str, item: str, post: Post):
        return post.update(self, name, item)

    def delete_post(self, post):
        return post.delete(self)
