from ..abstract_dto import Dto
from ...enums.report_type_enums import ReportType


class ReportCommentRequestDto(Dto):
    comment_id: str
    report_type: ReportType
    report_msg: str

