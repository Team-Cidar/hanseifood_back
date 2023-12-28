import logging

from .abstract_service import AbstractService

logger = logging.getLogger(__name__)


class BackOfficeService(AbstractService):
    def __init__(self):
        # add repository instance variables
        pass

    def add_menus(self):
        ...
