from openpyxl import Workbook, load_workbook
from matplotlib import pyplot as plt
import os
import numpy as np


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

def show_util_cpu(t, cpu, qcpu):
    np_x = np.asarray(t)
    np_y1 = np.asarray(cpu)
    np_y2 = np.asarray(q_cpu)

    fig, ax = plt.subplots()
    ax.plot(np_x, np_y1, color='blue', label='Утилизация CPU')
    ax.plot(np_x, np_y2, color='green', label='Очередь CPU')
    ax.set_xlabel('Продолжительность теста, ч:мм')
    ax.set_ylabel('Утилизация CPU, %')
    ax.set_title('Утилизация CPU')
    plt.legend(loc='upper left')
    ylim = ax.get_ylim()

    sub_ax = ax.twinx()
    sub_ax.plot([], [])
    sub_ax.set_ylabel('Очереди CPU, шт')
    sub_ax.set_ylim(ylim[0], ylim[1])
    plt.grid()

    plt.show()


#=========   MAIN CODE ===============================
# Формируем имя файла
#f_name = 'Report_'+datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")+'.xlsx'
f_name_report = "Report.xlsx"
f_name_with_data = "sar_mpgu_izh.csv"

data = []
cpu = []
q_cpu = []
t = []

# делаем екселевский файл
Items = ['Graphs', 'CPU', 'MEM', 'DISK', 'NET', 'LOAD_AVG']

if os.path.exists(f_name_report):
    wb_report = load_workbook(f_name_report)
    for i in range(1, len(Items)):
        tmp_sheet = wb_report[Items[i]]
        wb_report.remove(tmp_sheet)
else:
    wb_report = Workbook()
    for item in Items:
        wb_report.create_sheet(item)
    wdel = wb_report['Sheet']
    wb_report.remove(wdel)

wb_report.save(f_name_report)

line = str('')

# Данные для CPU
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[1]]
    # Утилизация CPU, idle в %
    while True:
        line = infile.readline().strip()
        if '%idle' in line:
            data = space_to_tab(line).split('\t')
            del data[1:10]
            data[0] = data[0][:5]
            active_sheet.cell(row = 1, column = 1).value = data[0]
            active_sheet.cell(row = 1, column = 2).value = data[1]
            break

    r = 2
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        if 'all' in line:
            data = space_to_tab(line).split('\t')
            del data[1:10]
            data[0] = data[0][:5]
            active_sheet.cell(row = r, column = 1).value = data[0]
            t.append(data[0])
            a = 100.0 - float(data[1].replace(',', '.'))
            active_sheet.cell(row = r, column = 2).value = a
            cpu.append(a)
            r += 1

    # очереди CPU
    while True:
        line = infile.readline().strip()
        if 'runq-sz' in line:
            data = space_to_tab(line).split('\t')
            del data[2:]
            active_sheet.cell(row = 1, column = 3).value = data[1]
            break

    r = 2
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[2:]
        a = float(data[1].replace(',', '.'))
        active_sheet.cell(row = r, column = 3).value = a
        q_cpu.append(a)
        r += 1

#Рисуем график 'Утилизация CPU' и 'Очереди CPU'
show_util_cpu(t, cpu, q_cpu)

# Данные для МЕМ
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[2]]
    while True:
        line = infile.readline().strip()
        if 'memused' in line:
            data = space_to_tab(line).split('\t')
            del data[1:3]
            del data[2:]
            data[0] = data[0][:5]
            active_sheet.cell(row = 1, column = 1).value = data[0]
            active_sheet.cell(row = 1, column = 2).value = data[1]
            break

    r = 2
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[1:3]
        del data[2:]
        data[0] = data[0][:5]
        active_sheet.cell(row = r, column = 1).value = data[0]
        active_sheet.cell(row = r, column = 2).value = float(data[1].replace(',', '.'))
        r += 1

    while True:
        line = infile.readline().strip()
        if 'swpused' in line:
            data = space_to_tab(line).split('\t')
            del data[1:3]
            del data[2:]
            active_sheet.cell(row=1, column=3).value = data[1]
            break

    r = 2
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[1:3]
        del data[2:]
        active_sheet.cell(row=r, column=3).value = float(data[1].replace(',', '.'))
        r += 1

# Данные для среднего времени чтения/записи
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[3]]
    while True:
        line = infile.readline().strip()
        if 'DEV' in line:
            data = space_to_tab(line).split('\t')
            del data[1:6]
            data[0] = data[0][:5]
            active_sheet.cell(row = 1, column = 1).value = data[0]
            active_sheet.cell(row = 1, column = 2).value = data[1]
            active_sheet.cell(row = 1, column = 3).value = data[2]
            active_sheet.cell(row = 1, column = 4).value = data[3]
            active_sheet.cell(row = 1, column = 5).value = data[4]
            break

    # САМЫЙ ЖОПОШНЫЙ УЧАСТОК КОДА
    map = {}
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[2:6]
        data[0] = data[0][:5]
        key = data[0]
        del data[0:2]
        if key in map.keys():
            map[key].append(data)
        else:
            map[key] = [data]


    size = len(map['09:21'])
    avg_map = {}
    rowNum = 2
    for key in map.keys():
        _avgqu_sz = 0.0
        _await = 0.0
        _svctm = 0.0
        _util = 0.0
        for i in map[key]:
            _avgqu_sz += float(i[0].replace(',', '.'))
            _await += float(i[1].replace(',', '.'))
            _svctm += float(i[2].replace(',', '.'))
            _util += float(i[3].replace(',', '.'))

        avg_map[key] = [_avgqu_sz / size, _await / size, _svctm / size, _util / size]
        active_sheet.cell(row=rowNum, column=1).value = key
        active_sheet.cell(row=rowNum, column=2).value = avg_map[key][0]
        active_sheet.cell(row=rowNum, column=3).value = avg_map[key][1]
        active_sheet.cell(row=rowNum, column=4).value = avg_map[key][2]
        active_sheet.cell(row=rowNum, column=5).value = avg_map[key][3]
        rowNum += 1

# Усредненные данные по сетевым интерфейсам
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[4]]
    while True:
        line = infile.readline().strip()
        if 'IFACE' in line:
            data = space_to_tab(line).split('\t')
            del data[1:4]
            del data[3:]
            data[0] = data[0][:5]
            active_sheet.cell(row=1, column=1).value = data[0]
            active_sheet.cell(row=1, column=2).value = data[1]
            active_sheet.cell(row=1, column=3).value = data[2]
            break

    map = {}
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[1:4]
        del data[3:]
        data[0] = data[0][:5]
        key = data[0]
        del data[0]
        if key in map.keys():
            map[key].append(data)
        else:
            map[key] = [data]

    size = len(map['09:21'])
    avg_map = {}
    rowNum = 2
    for key in map.keys():
        rxkB = 0.0
        txkB = 0.0
        for i in map[key]:
            rxkB += float(i[0].replace(',', '.'))
            txkB += float(i[1].replace(',', '.'))
        avg_map[key] = [rxkB/size, txkB/size]
        active_sheet.cell(row=rowNum, column=1).value = key
        active_sheet.cell(row=rowNum, column=2).value = avg_map[key][0]
        active_sheet.cell(row=rowNum, column=3).value = avg_map[key][1]
        rowNum += 1

# Динамика Load Average
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[5]]
    while True:
        line = infile.readline().strip()
        if 'runq-sz' in line:
            data = space_to_tab(line).split('\t')
            del data[1:3]
            data[0] = data[0][:5]
            active_sheet.cell(row = 1, column = 1).value = data[0]
            active_sheet.cell(row = 1, column = 2).value = data[1]
            active_sheet.cell(row = 1, column = 3).value = data[2]
            active_sheet.cell(row = 1, column = 4).value = data[3]
            break

    r = 2
    while True:
        line = infile.readline().strip()
        if 'Average' in line:
            break
        data = space_to_tab(line).split('\t')
        del data[1:3]
        data[0] = data[0][:5]
        active_sheet.cell(row=r, column=1).value = data[0]
        active_sheet.cell(row=r, column=2).value = float(data[1].replace(',', '.'))
        active_sheet.cell(row=r, column=3).value = float(data[2].replace(',', '.'))
        active_sheet.cell(row=r, column=4).value = float(data[3].replace(',', '.'))
        r += 1

wb_report.save(f_name_report)

#Начинаем рисовать
