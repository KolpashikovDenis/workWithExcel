import openpyxl

def space_to_tab(line):
    c = []
    i = 0
    while i < len(line):
        if line[i] == ' ':
            c.append('\t')
            while line[i] == ' ':
                i += 1
        else:
            c.append(line[i])
        i += 1

    line = ''.join(c)
    return line


f_name = 'sar_mpgu_izh.csv'


with open(f_name, 'r') as rdfile:
    while True:
        line = rdfile.readline().strip()
        if line == '':
            rdfile.readline().strip()
            break

    while True:
        line = rdfile.readline().strip()
        space_to_tab(line)
        print(line)