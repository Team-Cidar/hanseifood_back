import logging


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', 'UNKNOWN')

        logger = logging.getLogger(__name__)
        logger.info(f'{client_ip} - Request "{request.method} {request.path}"')  # 요청 들어왔을 때

        response = self.get_response(request)

        logger.info(f"{client_ip} - Response \"{request.method} {request.path}\" {response.status_code}")  # 응답 나가기 전
        return response