from flask_restful import Resource
from flask_login import login_user, logout_user
from app.resources.lib import api_response


class AuthAPI(Resource):
    @staticmethod
    def post():
        """
        Handle user login.

        # TODO (@gzhou): Need to take in user data for authentication checks.
        :return: JSON response
        """
        from app.database.user import get_first, create
        user = get_first()
        if user is None:
            user = create("GUID", "EDIRSSO", "Dirk", None, "Diggler", "doubled@email.com")
        login_user(user)
        return api_response.success()

    @staticmethod
    def delete():
        """
        Handle user logout.

        # TODO (@gzhou): Need to take in user session to delete user session from session store.
        :return: JSON response
        """
        logout_user()
        return api_response.success()
