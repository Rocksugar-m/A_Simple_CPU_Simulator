insts = ['LD F6 34+ R2', 'LD F2 45+ R3', 'MULTD F0 F2 F4', 'SUBD F8 F6 F2', 'DIVD F10 F0 F6', 'ADDD F6 F8 F2']
Funname = [['Integer', 1], ['Mult1', 10], ['Mult2', 10], ['ADD', 2], ['Divide', 40]]
splitinsts = []
INSTS = [[0] * 4 for row in range(len(insts))]  # Instruction status
FUNUS = [['/'] * 9 for row in range(5)]  # Functional unit status
for i in range(5):
    FUNUS[i][0] = 'NO'
REG = ['/'] * 16  # Register result status
finish = len(insts)
Clock = 1
temp = [-1 for i in range(len(insts))]
for i in range(len(insts)):  # 分割指令，取出指令用到的寄存器
    temp1 = []
    for j in range(4):
        temp1.append(insts[i].split()[j])
    splitinsts.append(temp1.copy())


def view():
    print("\n\nCLOCK:  " + str(Clock))
    print("Instruction status:")
    for i in range(len(INSTS)):
        print(INSTS[i])
    print("Functional unit status:")
    for i in range(len(FUNUS)):
        print(FUNUS[i])
    print("Register result status:")
    print(REG)


def classinst(op):
    if op == 'LD':
        if FUNUS[0][0] == 'NO':
            return 0
        else:
            return -1
    elif op == 'MULTD':
        if FUNUS[1][0] == 'NO':
            return 1
        elif FUNUS[2][0] == 'NO':
            return 2
        else:
            return -1
    if (op == 'ADDD') | (op == 'SUBD'):
        if FUNUS[3][0] == 'NO':
            return 3
        else:
            return -1
    if op == 'DIVD':
        if FUNUS[4][0] == 'NO':
            return 4
        else:
            return -1


def AddFun(Tname, i):
    temp[i] = Tname
    FUNUS[Tname][0] = 'YES'
    FUNUS[Tname][1] = splitinsts[i][0]
    FUNUS[Tname][2] = splitinsts[i][1]
    if splitinsts[i][2].find('F') >= 0:
        FUNUS[Tname][3] = splitinsts[i][2]
    else:
        FUNUS[Tname][3] = '/'
    FUNUS[Tname][4] = splitinsts[i][3]


def fun():
    for i in range(5):
        if FUNUS[i][0] == 'YES':
            if FUNUS[i][3].find('F') >= 0:
                FUNUS[i][5] = REG[int(int(FUNUS[i][3].split('F')[1]) / 2)]
            else:
                FUNUS[i][5] = '/'
            if FUNUS[i][4].find('F') >= 0:
                FUNUS[i][6] = REG[int(int(FUNUS[i][4].split('F')[1]) / 2)]
            else:
                FUNUS[i][6] = '/'
            if FUNUS[i][5] != '/':
                FUNUS[i][7] = 'NO'
            else:
                FUNUS[i][7] = 'YES'
            if FUNUS[i][6] != '/':
                FUNUS[i][8] = 'NO'
            else:
                FUNUS[i][8] = 'YES'
            REG[int(int(FUNUS[i][2].split('F')[1]) / 2)] = Funname[i][0]


def findwar(num):
    return 1


def scoreb(insts):
    global Clock
    global finish
    global REG
    global FUNUS
    global INSTS
    global temp
    a = []
    while finish != 0:
        for i in range(len(insts)):
            Tname = classinst(splitinsts[i][0])
            if ((i == 0) & (Clock == 1) | (
                    (INSTS[i][0] == 0) & (INSTS[i - 1][0] != 0) & (INSTS[i - 1][0] != Clock) & (Tname >= 0))):
                INSTS[i][0] = Clock
                AddFun(Tname, i)
            if temp[i] != -1:
                if (INSTS[i][3] == 0) & (INSTS[i][2] != 0) & (INSTS[i][2] != Clock) & (
                        Funname[temp[i]][0] == REG[int(int(splitinsts[i][1].split('F')[1]) / 2)]) & (
                        findwar(int(splitinsts[i][1].split('F')[1]))):
                    INSTS[i][3] = Clock
                    aaa = [int(int(splitinsts[i][1].split('F')[1]) / 2), temp[i]]
                    a.append(aaa.copy())
                    finish = finish - 1
                if (INSTS[i][1] == 0) & (INSTS[i][0] != 0) & (INSTS[i][0] != Clock) & (FUNUS[temp[i]][7] == 'YES') & (
                        FUNUS[temp[i]][8] == 'YES'):
                    INSTS[i][1] = Clock
                if (INSTS[i][2] == 0) & (INSTS[i][1] != 0) & (Clock == INSTS[i][1] + Funname[temp[i]][1]):
                    INSTS[i][2] = Clock
            fun()
        for j in range(len(a)):
            REG[a[0][0]] = '/'
            FUNUS[a[0][1]][0] = 'NO'
            a.pop(0)
        view()
        Clock = Clock + 1


scoreb(insts)
