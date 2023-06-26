import pandas as pd
import datetime as dt

filename = 'test1.xlsx'
engine = 'openpyxl'

# 읽어올 시작 행, 열의 인덱스 (0부터 시작)
start_row = 4
start_col = 2

# 읽어올 마지막 행, 열의 인덱스 (0부터 시작)
end_row = 11
end_col = 6

excel = pd.read_excel(filename, engine=engine).iloc[start_row-1:end_row, start_col-1:end_col]

excel.drop(4, inplace=True)
excel = excel.transpose()

result = {}
year = str(dt.datetime.now())[0:4]

for idx, item in enumerate(excel.values):
    key = item[0]
    key = key[4:9].replace('.', '-')
    key = year + "-" + key
    result[key] = list(item[1:])
print(result)
