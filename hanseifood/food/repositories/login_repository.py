from django.db.models import Model, QuerySet

from ..models import CustomUser


class LoginRepository:
    def __init__(self):
        pass

    def createUser(self, id, nickname):
        entity = CustomUser(username=id, kakaonickname=nickname)
        entity.set_password(nickname)
        entity.save()
        return entity

    def saveNickName(self,id, customnickname):
        entity = CustomUser.objects.filter(username=id).first()
        entity.nickname = customnickname
        entity.save()
        return entity

    def findByID(self, id) -> QuerySet:
        datas: QuerySet = CustomUser.objects.filter(username=id).first()
        return datas

    def findByID2(self, id) -> QuerySet:
        datas: QuerySet = CustomUser.objects.filter(username=id, nickname="").first()
        return datas
