from datetime import datetime
from openpyxl import Workbook
from openpyxl.writer.excel import save_workbook

def space_to_tab(line):
    c = []
    i = 0
    while i < len(line):
        if line[i] == ' ':
            c.append('\t')
            while line[i] == ' ':
                i += 1
            c.append(line[i])
        else:
            c.append(line[i])
        i += 1

    line = ''.join(c)
    return line



#=========   MAIN CODE ===============================
# Формируем имя файла
f_name = "Report_%Y-%m-%d_%H-%M-%S"
print(datetime.now().strptime())

data = []
book = Workbook()

# делаем екселевский файл
Items = ['Graphs', 'CPU', 'MEM', 'DISK', 'NET']
wb_report = Workbook()
for item in Items:
    wb_report.create_sheet(item)

with open(f_name, 'r') as rdfile:
    while True:
        line = rdfile.readline().strip()
        if line == '':
            line = rdfile.readline().strip()
            c = line.split('\t')
            break

    while True:
        line = rdfile.readline().strip()
        if line == '':
            break
        if 'all' in line:
            data.append(space_to_tab(line).split('\t'))
            # TODO: чтение выхлапа sar, создание первой диаграммы
            #print(data)
        else:
            continue

    print('----------------------------------------------------------------------------')

    while True:
        line = rdfile.readline().strip()
        if line == '':
            break
        if 'all' in line:
            data = space_to_tab(line).split('\t')
            # TODO: чтение выхлапа sar, создание первой диаграммы
            print(data)
        else:
            continue

    print('----------------------------------------------------------------------------')
