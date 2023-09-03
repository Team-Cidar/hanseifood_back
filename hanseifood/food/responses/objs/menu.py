from .abstract_model import AbstractModel


class MenuModel(AbstractModel):
    # 여기에 필드 선언하면 static field
    def __init__(self):
        # 이렇게 선언하면 instance field
        self.only_employee = True
        self.has_additional = False
        self.student_menu = dict()
        self.employee_menu = dict()
        self.additional_menu = dict()

    # override
    def __add__(self, model):
        self.student_menu.update(model.student_menu)
        self.employee_menu.update(model.employee_menu)
        self.additional_menu.update(model.additional_menu)
        self.has_additional |= model.has_additional
        self.only_employee &= model.only_employee
        return self

    # override
    def _AbstractModel__serialize(self) -> dict:  # 추상 메서드가 private이라 재정의 할 때 _추상클래스__method() 이런식으로 해줘야함
        return {
            'only_employee': self.only_employee,
            'has_additional': self.has_additional,
            'student_menu': self.student_menu,
            'employee_menu': self.employee_menu,
            'additional_menu': self.additional_menu
        }