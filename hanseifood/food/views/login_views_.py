from ..models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
import json
import requests
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect


id = None
nickname = None
token = None

KAKAO_REST_API_KEY = 'c8300aee5549fc7db67a25a714144789'
kakao_token_api = 'https://kauth.kakao.com/oauth/token'



@method_decorator(csrf_exempt,name='dispatch')
def getInfo(request):
    if request.method == "POST":
        a = 10
    return HttpResponse(a)




@method_decorator(csrf_exempt,name='dispatch')
def gettoken(request):
    print("hi")
    global token
    global id
    global nickname
    if request.method == "POST":

        code = json.loads(request.body).get("code")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        body = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_REST_API_KEY,
            'redirect_uri': 'http://localhost:8080/login/confirm',
            'code': code,
        }

        response = requests.post(kakao_token_api, headers=headers, data=body)

        data = response.json()
        token = data.get('access_token')

        headers = {
            'Authorization': f'Bearer ${token}'
        }
        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)

        data = response.json()
        id = data.get('id')
        data2 = data.get('properties')
        nickname = data2.get('nickname')
        failed_data = {
            "id": id,
            "nickname": nickname,
            "isExists": "false"
                }
        success_data = {
            "id":id,
            "nickname":nickname,
            "isExists": "true"
        }
        existing_user = CustomUser.objects.filter(username=id).first()
        existing_user2 = CustomUser.objects.filter(username=id,nickname="").first()
        print(existing_user)
        if existing_user is None:
            user, created = CustomUser.objects.get_or_create(username=id, kakaonickname=nickname)
            user.set_password(nickname)
            user.save()
            return JsonResponse(failed_data)
        elif existing_user2:
            return JsonResponse(failed_data)
        else:
            return JsonResponse(success_data)

# @method_decorator(csrf_exempt, name='dispatch')
# def verify_user(request):
#     if request.method == "POST":
#         print(id)
#
#         existing_user2 = CustomUser.objects.filter(userid=id).first()
#
#         if existing_user2 is not None:
#
#             # 이미 존재하는 ID인 경우에 대한 처리를 여기에 추가
#
#             return HttpResponse("이미 생성된 사용자임", status=500)
#         else:
#             # ID가 존재하지 않으면 새로운 사용자 생성
#
#
#             return HttpResponse("사용자 생성 완료", status=200)

        # user, created = User.objects.get_or_create(username=id)
        # user.set_password("1234")
        # user.save()
        # response_data = {'id': id}

    # return JsonResponse(response_data)

@method_decorator(csrf_exempt,name='dispatch')
def get_user_info(request):
    if request.method == "POST":

        customnickname=json.loads(request.body).get("nickname")


        print(id)
        print(customnickname)
        # 이미 존재하는 ID인지 확인
        new_user = CustomUser.objects.filter(username=id).first()
        print(new_user)

        # if nonickname_user is None:
        #
        #     return HttpResponse("이미 생성된 사용자임", status=500)
        #
        # else:
        #     # 이미 존재하는 ID인 경우에 대한 처리를 여기에 추가
        #     if customnickname == '':
        #         return HttpResponse("공백 꺼지삼", status=500)
        #     else:
        #         nonickname_user.nickname = customnickname
        #         nonickname_user.save()
        new_user.nickname = customnickname
        new_user.save()

        return HttpResponse("사용자 생성 완료", status=200)



@method_decorator(csrf_exempt,name='dispatch')
def logout(request):
    if request.method == "POST":

        print(token)
        response = requests.get('https://kauth.kakao.com/oauth/logout?client_id=c8300aee5549fc7db67a25a714144789&logout_redirect_uri=http://localhost:8080')
        if response.status_code == 200:
            return HttpResponse('로그아웃되었습니다.', status=200)
        else:
            return HttpResponse('로그아웃에 실패했습니다.', status=response.status_code)

    return HttpResponse('잘못된 요청입니다.', status=400)

@method_decorator(csrf_exempt,name='dispatch')
def getInfo(request):
    if request.method == "POST":

        return HttpResponse('너만봐.', status=200)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_staff']=user.is_staff #확장
        token['is_superuser']=user.is_superuser #확장
        token['nickname']=user.nickname
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
