import re

from .post_model import Post, posts_list, UpdateError
from .user_model import User, users_list

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
password_pattern = re.compile(r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")
