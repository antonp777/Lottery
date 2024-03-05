from app.Models.UserAdmin import UserAdmin
from app.dao.BaseDAO import BaseDAO


class UserAdminDAO(BaseDAO):
    model = UserAdmin
