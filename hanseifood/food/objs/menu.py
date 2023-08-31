from .abstract_model import AbstractModel


class MenuModel(AbstractModel):
    # 여기에 필드 선언하면 static field
    def __init__(self, date):
        # 이렇게 선언하면 instance field
        self.date = date
        self.only_employee = False
        # self.has_two_menus = False
        self.student_menu = []
        self.employee_menu = []

    # override
    def _AbstractModel__serialize(self) -> dict:  # 추상 메서드가 private이라 재정의 할 때 _추상클래스__method() 이런식으로 해줘야함
        return {
            'date': self.date,
            'only_employee': self.only_employee,
            # 'has_two_menus': self.has_two_menus,
            'student_menu': self.student_menu,
            'employee_menu': self.employee_menu,
        }

