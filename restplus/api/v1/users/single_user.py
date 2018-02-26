from flask import redirect
from flask_login import current_user, login_required
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from restplus.api.v1.helpers import safe_user_output, check_id_availability
from restplus.models import users_list, User
from ..auth.logout import Logout

users_ns = Namespace('users')


class SingleUser(Resource):
    def get(self, user_id: int):
        return dict(user=safe_user_output(self, check_id_availability(self, user_id, users_list, str(User.__name__))))

    @login_required
    def delete(self, user_id: int):
        if current_user.id != user_id:
            users_ns.abort(403)

        this_user = check_id_availability(self, user_id, users_list, str(User.__name__))

        users_list.remove(this_user)
        return redirect(self.api.url_for(Logout), 204)
