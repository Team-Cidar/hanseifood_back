from datetime import datetime

from .user_dto import UserDto
from ..abstract_dto import Dto
from ...enums.report_type_enums import ReportType
from ...models import CommentReport


class CommentReportDto(Dto):
    def __init__(self, reporter: UserDto, report_type: ReportType):
        self.comment_id: str = ''
        self.reporter: UserDto = reporter
        self.report_type: ReportType = report_type
        self.report_msg: str = ''
        self.reported_at: datetime = datetime.today()

    @classmethod
    def from_model(cls, model: CommentReport):
        dto: CommentReportDto = cls(
            reporter=UserDto.from_model(model.reporter),
            report_type=ReportType.from_value(model.report_type)
        )
        dto.comment_id = str(model.comment_id)
        dto.report_msg = str(model.report_msg)
        dto.reported_at = model.reported_at
        return dto
