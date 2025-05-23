from app.base_dao import BaseDAO
from app.business_logic.applications.models import Application


class ApplicationsDAO(BaseDAO):
    model = Application
