import pandas as pd
import datetime as dt
from ...utils.date_utils import get_week_number


class ExcelParser:
    @staticmethod
    def _parse_students_menu(excel_df):
        df = excel_df.iloc[3:11, 1:7]  # get only menu range
        df = df.transpose()
        # fill Nan data in date column as the right before data (e.g. mon tue wed Nan thu fri => mon tue wed wed thu fri)
        df.iloc[:, :1] = df.iloc[:, :1].fillna(method='ffill')
        df.iloc[:, :2] = df.iloc[:, :2].fillna(value='all')
        df.fillna(value=0, inplace=True)  # replace all extra Nan datas as 0

        daily_menus = {}
        cur_year = str(dt.datetime.today().year)
        for item in df.values.tolist():
            key = cur_year + '-' + item[0][4:9].replace('.', '-')
            target_restaurant = item[1]
            menus = [menu for menu in item[2:] if menu != 0]  # remove all 0 data

            """ version1
            학생식당, 교직원식당 나눠져있는 경우 list<dict> 타입으로 예를 들어 아래와 같이 표현
            {
                ...,
                수: [
                        {학생식당: [메뉴 리스트]},
                        {교직원식당: [메뉴 리스트]}
                    ],
                ...
            }
            """
            # if target_restaurant != 'all':
            #     if key in daily_menus.keys():  # if key already exists in the result
            #         daily_menus[key].append({target_restaurant: menus})
            #     else:  # key is not exists in the result
            #         daily_menus[key] = [{target_restaurant: menus}]
            # else:  # same menu to both students and employees
            #     daily_menus[key] = menus

            """version 2
           학생식당, 교직원식당 나눠져있는 경우 list<list> 타입으로 예를 들어 아래와 같이 표현 
            {
                ...,
                수: [
                        [메뉴 리스트],
                        [메뉴 리스트],
                    ],
                ...
            }
            ## list[수][0] = 학생식당,
            ## list]수][1] = 직원식당
            """
            if target_restaurant != 'all':
                if key in daily_menus.keys():
                    daily_menus[key] = [daily_menus[key], menus]
                    continue
            daily_menus[key] = menus

        return daily_menus

    @staticmethod
    def _parse_employee_menu(excel_df):
        # 읽어올 시작 행, 열의 인덱스 (0부터 시작)
        start_row = 4
        start_col = 2

        # 읽어올 마지막 행, 열의 인덱스 (0부터 시작)
        end_row = 11
        end_col = 6

        excel = excel_df.iloc[start_row - 1:end_row, start_col - 1:end_col]

        excel.drop(4, inplace=True)
        excel = excel.transpose()

        excel.fillna(value=0, inplace=True)

        result = {}
        year = str(dt.datetime.now())[0:4]

        for idx, item in enumerate(excel.values):
            key = item[0]
            key = key[4:9].replace('.', '-')
            key = year + "-" + key
            result[key] = [i for i in item[1:] if i != 0]

        return result

    @staticmethod
    def parse_excel(file_path):
        pages: dict = pd.read_excel(file_path, engine='openpyxl', sheet_name=None)
        # check if it has two or more week's menu datas
        if len(pages) == 1:
            excel_pd = list(pages.values())[0]
        else:
            week_num = get_week_number()
            excel_pd = list(pages.values())[week_num - 1]

        if len(excel_pd.columns) == 12:
            return ExcelParser._parse_employee_menu(excel_pd), False
        else:
            return ExcelParser._parse_students_menu(excel_pd), True


if __name__ == "__main__":
    print('parse_test')
