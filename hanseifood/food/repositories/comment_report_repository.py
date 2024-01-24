from typing import Tuple

from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..enums.report_type_enums import ReportType
from ..models import User, CommentReport


class CommentReportRepository(AbstractRepository):
    def __init__(self):
        super(CommentReportRepository, self).__init__(CommentReport.objects)

    # override
    def save(self, comment_id: str, reporter: User, report_type: ReportType, report_msg: str) -> CommentReport:
        entity: CommentReport = CommentReport(
            comment_id=comment_id,
            reporter=reporter,
            report_type=report_type.value,
            report_msg=report_msg
        )
        entity.save()
        return entity
