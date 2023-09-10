class ParseObject:
    def __init__(self):
        self.keys = list()
        self.students = dict()
        self.employees = dict()
        self.additional = dict()

    def to_dict(self):
        return {
            'keys': self.keys,
            'students': self.students,
            'employee': self.employees,
            'additional': self.additional
        }
