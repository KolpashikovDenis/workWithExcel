from openpyxl import Workbook

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
#f_name = 'Report_'+datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")+'.xlsx'
f_name_report = "Report.xlsx"
f_name_with_data = "sar_mpgu_izh.csv"

data = []
# CPU = []
# MEM = []
# #DISK = [] ------ ????????
# NET = [] # ??????

# делаем екселевский файл
Items = ['Graphs', 'CPU', 'MEM', 'DISK', 'NET']
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
    while True:
        line = infile.readline().strip()
        if '%idle' in line:
            data = space_to_tab(line).split('\t')
            del data[1:10]
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
            active_sheet.cell(row = r, column = 1).value = data[0]
            active_sheet.cell(row = r, column = 2).value = data[1]
            r += 1

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
        active_sheet.cell(row = r, column = 3).value = data[1]
        r += 1

# Данные для МЕМ
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[2]]
    while True:
        line = infile.readline().strip()
        if 'memused' in line:
            data = space_to_tab(line).split('\t')
            del data[1:3]
            del data[2:]
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
        active_sheet.cell(row = r, column = 1).value = data[0]
        active_sheet.cell(row = r, column = 2).value = data[1]
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
        active_sheet.cell(row=r, column=3).value = data[1]
        r += 1

# Данные для среднего времени чтения/записи
with open(f_name_with_data, 'r') as infile:
    active_sheet = wb_report[Items[3]]
    while True:
        line = infile.readline().strip()
        if 'DEV' in line:
            data = space_to_tab(line).split('\t')
            del data[1:6]
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
        key = data[0]
        del data[0:2]
        if key in map.keys():
            map[key].append(data)
        else:
            map[key] = [data]


    size = len(map['09:21:06'])
    # _avgqu_sz = 0.0
    # _await = 0.0
    # _svctm = 0.0
    # _util = 0.0
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

    print()

#

wb_report.save(f_name_report)
