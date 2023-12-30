from django.http import HttpResponse

from .abstract_response import AbstractResponse


class FileResponse(AbstractResponse):
    @staticmethod
    def response(file_path: str, content_type: str, status_code: int = 200) -> HttpResponse:
        with open(file_path, 'rb') as file:
            response = HttpResponse(content=file.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename={file_path.split("/")[1]}'
            return response
