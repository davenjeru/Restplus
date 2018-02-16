import datetime
import re

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

users_list = []
posts_list = []

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
password_pattern = re.compile(r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")


class User(UserMixin, object):
    """
    This is the user class.
    Defines a user and all actions that can be done by it.
    """

    id = 1

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
        self.id = User.id

    def save(self):
        User.id += 1
        users_list.append(self)

    def get_id(self):
        return chr(self.id)

    def authenticate(self, password):
        return check_password_hash(self.password, password)

    @property
    def serialize(self):
        return {'email': self.email}

    def create_post(self, title, body):
        my_post = Post(self, title, body)
        my_post.save()
        return my_post


class Post(object):
    id = 1

    def __init__(self, user, title, body):
        self.id = Post.id
        self.user_id = user.id
        self.title = title
        self.body = body
        self.created_on = datetime.datetime.now()
        self.last_modified = None

    def save(self):
        Post.id += 1
        posts_list.append(self)

    @property
    def serialize(self):
        return dict(title=self.title, body=self.body, created_on=str(self.created_on),
                    last_modified=self.last_modified)
