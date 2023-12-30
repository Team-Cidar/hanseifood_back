from .abstract_model import AbstractModel


class MenuModificationModel(AbstractModel):
    def __init__(self, is_new: bool):
        self.is_new: bool = is_new

    def _serialize(self) -> dict:
        return {
            "is_new": self.is_new
        }
