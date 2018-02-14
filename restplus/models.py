import re

from werkzeug.security import generate_password_hash

users_list = []

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
password_pattern = re.compile(r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")


class User(object):
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
