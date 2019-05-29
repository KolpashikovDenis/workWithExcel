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
f_name = 'sar_mpgu_izh.csv'

data = []
book = Workbook()


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

