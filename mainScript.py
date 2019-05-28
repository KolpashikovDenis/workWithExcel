from datetime import datetime
from openpyxl import Workbook
from openpyxl.writer.excel import save_workbook

def space_to_tab(_line):
    c = []
    i = 0
    while i < len(_line):
        if _line[i] == ' ':
            c.append('\t')
            while _line[i] == ' ':
                i += 1
        else:
            c.append(_line[i])
        i += 1

    _line = ''.join(c)
    return _line


#========================= MAIN CODE  =====================================================================
# Формируем имя файла
f_name = "Report_%Y-%m-%d_%H-%M-%S"
print(datetime.now().strptime())

# делаем екселевский файл
Items = ['Graphs', 'CPU', 'MEM', 'DISK', 'NET']
wb_report = Workbook()
for item in Items:
    wb_report.create_sheet(item)



#
#
# f_name = 'sar_mpgu_izh.csv'
#
# with open(f_name, 'r') as rdfile:
#     while True:
#         line = rdfile.readline().strip()
#         if line == '':
#             rdfile.readline().strip()
#             break
#
#     while True:
#         line = rdfile.readline().strip()
#         if line == '':
#             break
#
#         space_to_tab(line)
#         print(line)