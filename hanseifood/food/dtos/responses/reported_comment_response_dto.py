from datetime import datetime

from .comment_response_dto import CommentResponseDto
from ..abstract_dto import Dto
from ..model_mapped.comment_report_dto import CommentReportDto
from ..model_mapped.user_dto import UserDto
from ...enums.report_type_enums import ReportType


class ReportedCommentResponseDto(Dto):
    def __init__(self, reported_comment: CommentReportDto, comment: CommentResponseDto):
        self.comment: CommentResponseDto = comment
        self.reporter: UserDto = reported_comment.reporter
        self.report_type: ReportType = reported_comment.report_type
        self.report_msg: str = reported_comment.report_msg
        self.reported_at: datetime = reported_comment.reported_at
