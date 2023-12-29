from .abstract_model import AbstractModel


class MenuModificationModel(AbstractModel):
    def __init__(self, is_created: bool):
        self.is_created: bool = is_created

    def _serialize(self) -> dict:
        return {
            "isCreated": self.is_created
        }
