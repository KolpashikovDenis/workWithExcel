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
f_name = 'Report_'+datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")+'.xlsx'

data = []
book = Workbook()

# делаем екселевский файл
Items = ['Graphs', 'CPU', 'MEM', 'DISK', 'NET']
wb_report = Workbook()

for item in Items:
    wb_report.create_sheet(item)
wdel = wb_report['Sheet']
wb_report.remove(wdel)
wb_report.save(f_name)

with open('sar_mpgu_izh.csv', 'r') as rdfile:
    # Пропустим первые две строки
    while True:
        line = rdfile.readline().strip()
        if line == '':
            break

    # Заполняем страничку с данными по CPU
    active_sheet = wb_report[Items[1]]

    _row = 1
    while True:
        line = rdfile.readline().strip()
        if (line == '') or ('Average' in line):
            break
        if 'all' in line:
            #data.append(space_to_tab(line).split('\t'))
            data = space_to_tab(line).split(('\t'))
            data.remove('all')
            # TODO: чтение выхлапа sar, создание первой диаграммы
            for i in range(1, len(data)+1):
                active_sheet.cell(row = _row, column = i).value = data[i - 1]
            _row += 1

        else:
            continue

    wb_report.save(f_name)
    print('----------------------------------------------------------------------------')

    active_sheet = wb_report[Items[2]]

    while True:
        line = rdfile.readline().strip()
        if line == '':
            break
        if 'all' in line:
            data = space_to_tab(line).split('\t')
            # TODO: чтение выхлапа sar, создание второй диаграммы
            print(data)
        else:
            continue

    print('----------------------------------------------------------------------------')
