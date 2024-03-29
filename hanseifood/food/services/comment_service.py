import logging
from typing import List

from django.core.paginator import Page
from django.db.models import QuerySet

from .abstract_service import AbstractService
from .menu_service import MenuService
from ..dtos.general.paging_dto import PagingDto, PagingResponseDto
from ..dtos.model_mapped.comment_deleted_dto import CommentDeletedDto
from ..dtos.model_mapped.comment_report_dto import CommentReportDto
from ..dtos.model_mapped.menu_comment_dto import MenuCommentDto
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..dtos.requests.delete_comment_request_dto import DeleteCommentRequestDto
from ..dtos.requests.get_comment_request_dto import GetCommentRequestDto
from ..dtos.requests.report_comment_request_dto import ReportCommentRequestDto
from ..dtos.responses.comment_response_dto import CommentResponseDto, DeletedCommentResponseDto
from ..dtos.responses.common_status_response_dto import CommonStatusResponseDto
from ..dtos.responses.menu_by_id_response_dto import MenuByIdResponseDto
from ..dtos.responses.reported_comment_response_dto import ReportedCommentResponseDto
from ..enums.report_type_enums import ReportType
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.jwt_exceptions import PermissionDeniedError
from ..exceptions.request_exceptions import EmptyValueError
from ..models import User, MenuComment
from ..repositories.comment_deleted_repository import CommentDeletedRepository
from ..repositories.comment_report_repository import CommentReportRepository
from ..repositories.menu_comment_repository import MenuCommentRepository

logger = logging.getLogger(__name__)


class CommentService(AbstractService):
    def __init__(self):
        self.__menu_comment_repository = MenuCommentRepository()
        self.__comment_report_repository = CommentReportRepository()
        self.__comment_deleted_repository = CommentDeletedRepository()
        self.__menu_service = MenuService()

    def add_comment(self, data: AddCommentRequestDto, user: User) -> CommentResponseDto:
        menu_dto: MenuByIdResponseDto = self.__menu_service.get_by_menu_id(data.menu_id)
        menu_comment: MenuComment = self.__menu_comment_repository.save(
            menu_id=data.menu_id,
            comment=data.comment,
            user_id=user
        )
        comment_dto: MenuCommentDto = MenuCommentDto.from_model(menu_comment)
        return CommentResponseDto(comment_dto, menu_dto)

    def delete_comment(self, data: DeleteCommentRequestDto, user: User):
        exists, comments = self.__menu_comment_repository.existByCommentId(comment_id=data.comment_id)
        if not exists:
            raise EmptyDataError(f"Comment with id '{data.comment_id}' is not exists")

        comment: MenuComment = comments[0]
        if user.role == UserRole.ADMIN:
            self.__menu_comment_repository.delete(comment)
            return CommonStatusResponseDto(True)

        if comment.user_id != user:
            raise PermissionDeniedError("Trying to delete other user's comment")

        self.__menu_comment_repository.delete(comment)
        return CommonStatusResponseDto(True)

    def get_comment_by_menu_id(self, data: GetCommentRequestDto, paging_data: PagingDto) -> PagingResponseDto:
        response: List[CommentResponseDto] = []
        exists, comments = self.__menu_comment_repository.existByMenuId(menu_id=data.menu_id)
        sorted_comments: QuerySet = comments.order_by('commented_at')
        page: Page = self.__menu_comment_repository.get_page(sorted_comments, paging_data)
        if not exists:
            return PagingResponseDto(page, response)

        menu_dto: MenuByIdResponseDto = self.__menu_service.get_by_menu_id(data.menu_id)
        for comment in page.object_list:
            comment_dto: MenuCommentDto = MenuCommentDto.from_model(comment)
            response.append(CommentResponseDto(comment_dto, menu_dto))

        return PagingResponseDto(page, response)

    def get_comment_by_user(self, user: User, paging_data: PagingDto) -> PagingResponseDto:
        comments: QuerySet = self.__menu_comment_repository.findByUserId(user_id=user)
        sorted_comments: QuerySet = comments.order_by('commented_at')
        page: Page = self.__menu_comment_repository.get_page(sorted_comments, paging_data)

        response: List[CommentResponseDto] = []
        comment: MenuComment
        for comment in page.object_list:
            menu_dto: MenuByIdResponseDto = self.__menu_service.get_by_menu_id(comment.menu_id)
            comment_dto: MenuCommentDto = MenuCommentDto.from_model(comment)
            response.append(CommentResponseDto(comment_dto, menu_dto))

        return PagingResponseDto(page, response)

    def report_comment(self, data: ReportCommentRequestDto, user: User) -> CommonStatusResponseDto:
        exists, comments = self.__menu_comment_repository.existByCommentId(data.comment_id)
        if not exists:
            raise EmptyDataError(f"Comment with id '{data.comment_id}' is deleted or not exists.")

        if data.report_type is not ReportType.ETC:
            data.report_msg = data.report_type.name
        else:
            if len(data.report_msg) == 0:
                raise EmptyValueError(msg=f'reportMsg field is required with ReportType.ETC. But not given.')

        self.__comment_report_repository.save(
            comment_id=data.comment_id,
            reporter=user,
            report_type=data.report_type,
            report_msg=data.report_msg
        )

        return CommonStatusResponseDto(True)

    def get_reported_comments(self, paging_data: PagingDto) -> PagingResponseDto:
        sorted_reported_comments: QuerySet = self.__comment_report_repository.all().order_by('reported_at').reverse()
        page: Page = self.__comment_report_repository.get_page(sorted_reported_comments, paging_data)

        reported_comments_dto: List[CommentReportDto] = [CommentReportDto.from_model(model) for model in page.object_list]
        response: List[ReportedCommentResponseDto] = []
        for r_comment_dto in reported_comments_dto:
            comment_response_dto: CommentResponseDto = self.get_by_comment_id(r_comment_dto.comment_id)
            response.append(ReportedCommentResponseDto(r_comment_dto, comment_response_dto))

        return PagingResponseDto(page, response)

    def get_by_comment_id(self, comment_id: str) -> CommentResponseDto:
        result: CommentResponseDto
        exists, comments = self.__menu_comment_repository.existByCommentId(comment_id)
        if not exists:
            exists, deleted_comments = self.__comment_deleted_repository.existByCommentId(comment_id)
            if not exists:
                raise EmptyDataError(f"Comment with id '{comment_id}' is not exists")
            deleted_dto = CommentDeletedDto.from_model(deleted_comments[0])
            menu_dto = self.__menu_service.get_by_menu_id(deleted_dto.menu_id)
            result = DeletedCommentResponseDto(deleted_dto, menu_dto)
        else:
            comment_dto = MenuCommentDto.from_model(comments[0])
            menu_dto = self.__menu_service.get_by_menu_id(comment_dto.menu_id)
            result = CommentResponseDto(comment_dto, menu_dto)
        return result