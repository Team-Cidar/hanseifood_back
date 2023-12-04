import json
import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (request.path.startswith('/login') or request.path.startswith('/api/token') or request.path.startswith('/nickname') or request.path.startswith('/admin')):
            AccessToken = request.headers.get("AccessToken")

            if AccessToken is not None:
                verify_token_url = 'http://127.0.0.1:8000/api/token/verify'


                try:
                    response = requests.post(verify_token_url, {
                    "token": AccessToken
                })

                    if response.status_code != 200:

                        return HttpResponse('토큰이 유효하지 않습니다.', status=500)

                except Exception as e:

                    return HttpResponse(f'오류 발생: {str(e)}', status=500)

            else: return HttpResponse('토큰이 존재하지 않습니다.', status=500)

        return self.get_response(request)
