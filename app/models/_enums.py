"""

    For enum types shared across models/tables.

"""

from app.database import db
from app.constants import user_auth_type


user_auth_type = db.Enum(
    user_auth_type.NYC_ID,
    user_auth_type.NYC_EMPLOYEES,
    user_auth_type.FACEBOOK,
    user_auth_type.MICROSOFT,
    user_auth_type.YAHOO,
    user_auth_type.LINKEDIN,
    user_auth_type.GOOGLE,
    name='user_auth_type'
)
