import pandas as pd
import datetime

from .objs.parse_obj import ParseObject

pd.set_option('max_rows', None)  # print row without collapsing
pd.set_option('display.width', None)  # print columns without collapsing
pd.set_option('max_colwidth', None)  # print every cells without collapsing


class TempExcelParser:
    @staticmethod
    def parse(file_path) -> ParseObject:
        excel: pd.DataFrame = pd.read_excel(file_path, engine='openpyxl')

        print(len(excel.columns))

        menus_with_target: pd.DataFrame = excel.iloc[3:11]  # 대상 포함
        menus_without_target: pd.DataFrame = menus_with_target.iloc[:, 1:]  # 대상 미포함

        menus: pd.DataFrame = menus_without_target.transpose()
        menus.drop(4, axis=1, inplace=True)  # drop useless column

        res = ParseObject()
        cur_year = datetime.datetime.today().year

        for daily_menus in menus.values:
            daily_menus = list(daily_menus)
            # format
            # [date, ...menus, std/emp_only, additional]

            date = daily_menus[0]  # dates

            base_menus = daily_menus[1:-1]

            base_for_student = base_menus[:-1]  # student menu
            base_for_student.append(base_menus[-1].split('/')[0])

            base_for_employee = base_menus[:-1]  # employee menu
            base_for_employee.extend(base_menus[-1].split('/'))

            additional_menus = daily_menus[-1].split('\n')  # additional menu

            key = f'{cur_year}-{date[4:9].replace(".", "-")}'

            res.keys.append(key)
            res.students[key] = base_for_student
            res.employees[key] = base_for_employee
            res.additional[key] = additional_menus

        return res


if __name__ == '__main__':
    pass
