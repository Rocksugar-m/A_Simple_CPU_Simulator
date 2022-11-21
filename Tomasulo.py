# 指令流，一个将数组各元素乘以一个常数的循环
insts = ['L.D F0,0(R1)', 'MUL.D F4,F0,F2', 'S.D 0(R1),F4', 'DADDUI R1,R1,#-8', 'BNE R1,R2,LOOP']

# 内存
ram = [1] * 1000

# 整数和浮点寄存器及其Qi(被哪个功能部件写)
reg_d = {'F0': 0, 'F2': 2, 'F4': 0}
reg_d_Q = {'F0': '', 'F2': '', 'F4': ''}
reg = {'R1': 80, 'R2': 0}
reg_Q = {'R1': '', 'R2': ''}

# 保留站
add_rs = {'add1': '', 'add2': '', 'add3': ''}
load_rs = {'load1': '', 'load2': ''}
store_rs = {'store1': '', 'store2': ''}
mult_rs = {'mult1': '', 'mult2': ''}


# 如果有对应的保留站为空，则可以发射
def ld_can_issue():
    for x in load_rs:
        if load_rs[x] == '':
            return x
    return ''


def sd_can_issue():
    for x in store_rs:
        if store_rs[x] == '':
            return x
    return ''


def add_can_issue():
    for x in add_rs:
        if add_rs[x] == '':
            return x
    return ''


def mult_can_issue():
    for x in mult_rs:
        if mult_rs[x] == '':
            return x
    return ''


pc = 0
clock = 0
current_load = ''
load_result = 0
load_clock = 0
current_store = ''
store_clock = 0
current_add = ''
add_result = 0
add_clock = 0
current_mult = ''
mult_result = 0
mult_clock = 0

# 广播计算结果，遍历所有保留站，将需要该结果的Vj Vk赋值并将Qj Qk赋空
def broadcast(function_unit, result):
    global load_rs
    global store_rs
    global add_rs
    global mult_rs
    for ld_rs in load_rs.values():
        if ld_rs == '':
            continue
        if ld_rs['Qj'] == function_unit:
            ld_rs['Qj'] = ''
            ld_rs['Vj'] = result
        if ld_rs['Qk'] == function_unit:
            ld_rs['Qk'] = ''
            ld_rs['Vk'] = result
    for sd_rs in store_rs.values():
        if sd_rs == '':
            continue
        if sd_rs['Qj'] == function_unit:
            sd_rs['Qj'] = ''
            sd_rs['Vj'] = result
        if sd_rs['Qk'] == function_unit:
            sd_rs['Qk'] = ''
            sd_rs['Vk'] = result
    for a_rs in add_rs.values():
        if a_rs == '':
            continue
        if a_rs['Qj'] == function_unit:
            a_rs['Qj'] = ''
            a_rs['Vj'] = result
        if a_rs['Qk'] == function_unit:
            a_rs['Qk'] = ''
            a_rs['Vk'] = result
    for m_rs in mult_rs.values():
        if m_rs == '':
            continue
        if m_rs['Qj'] == function_unit:
            m_rs['Qj'] = ''
            m_rs['Vj'] = result
        if m_rs['Qk'] == function_unit:
            m_rs['Qk'] = ''
            m_rs['Vk'] = result


def exe_write():
    global load_rs
    global store_rs
    global add_rs
    global mult_rs
    global current_load
    global load_result
    global load_clock
    global current_store
    global store_clock
    global current_add
    global add_result
    global add_clock
    global current_mult
    global mult_result
    global mult_clock
    # 当各功能部件中的指令的操作数准备好后，执行该指令
    for ld_rs in load_rs:
        if current_load == '' and load_rs[ld_rs] != '' and load_rs[ld_rs]['Qj'] == '' and load_rs[ld_rs]['Qk'] == '':
            load_rs[ld_rs]['A'] = load_rs[ld_rs]['Vj'] + load_rs[ld_rs]['A']
            load_result = ram[load_rs[ld_rs]['A']]
            current_load = ld_rs
            load_clock = clock
    for sd_rs in store_rs:
        if current_store == '' and store_rs[sd_rs] != '' and store_rs[sd_rs]['Qj'] == '' and store_rs[sd_rs]['Qk'] == '':
            store_rs[sd_rs]['A'] = store_rs[sd_rs]['Vj'] + store_rs[sd_rs]['A']
            ram[store_rs[sd_rs]['A']] = store_rs[sd_rs]['Vk']
            current_store = sd_rs
            store_clock = clock
    for a_rs in add_rs:
        if current_add == '' and add_rs[a_rs] != '' and add_rs[a_rs]['Qj'] == '' and add_rs[a_rs]['Qk'] == '':
            add_result = add_rs[a_rs]['Vj'] + add_rs[a_rs]['A']
            current_add = a_rs
            add_clock = clock
    for m_rs in mult_rs:
        if current_mult == '' and mult_rs[m_rs] != '' and mult_rs[m_rs]['Qj'] == '' and mult_rs[m_rs]['Qk'] == '':
            mult_result = mult_rs[m_rs]['Vj'] * mult_rs[m_rs]['Vk']
            current_mult = m_rs
            mult_clock = clock
    # 当指令执行完成后，写回结果并释放功能部件
    if current_load != '' and (clock - load_clock) >= 1:
        load_clock = 10000  # 这个clock用于记录该指令开始执行的时刻，并模拟其执行延迟
        broadcast(current_load, load_result)
        for index in reg_d:
            if reg_d_Q[index] == current_load:
                reg_d[index] = load_result
                reg_d_Q[index] = ''
        load_rs[current_load] = ''
        current_load = ''  # 记录当前占用功能部件的保留站
    if current_store != '' and (clock - store_clock) >= 1:
        store_clock = 10000
        store_rs[current_store] = ''
        current_store = ''
    if current_add != '' and (clock - add_clock) >= 2:
        add_clock = 10000
        broadcast(current_add, add_result)
        for index in reg:
            if reg_Q[index] == current_add:
                reg[index] = add_result
                reg_Q[index] = ''
        add_rs[current_add] = ''
        current_add = ''
    if current_mult != '' and (clock - mult_clock) >= 6:
        mult_clock = 10000
        broadcast(current_mult, mult_result)
        for index in reg_d:
            if reg_d_Q[index] == current_mult:

                reg_d[index] = mult_result
                reg_d_Q[index] = ''

        mult_rs[current_mult] = ''
        current_mult = ''


while pc != -1:
    # 发射，不同类型指令需满足tomasulo算法的条件
    inst = insts[pc]
    op = inst.split(' ')[0]
    if op == 'L.D':
        ld_rs = ld_can_issue()
        if ld_rs != '':
            rs = inst.split(' ')[1].split(',')[1][2:4]
            rt = inst.split(' ')[1].split(',')[0]
            offset = inst.split(' ')[1].split(',')[1][0]
            offset = int(offset)
            if reg_Q[rs] == '':
                Qj = ''
                Vj = reg[rs]
            else:
                Qj = reg_Q[rs]
                Vj = 0
            reg_d_Q[rt] = ld_rs
            load_rs[ld_rs] = {'Op': 'L.D', 'Qj': Qj, 'Qk': '', 'Vj': Vj, 'Vk': 0, 'A': offset, 'Busy': 1}
            pc += 1
    elif op == 'S.D':
        sd_rs = sd_can_issue()
        if sd_rs != '':
            rs = inst.split(' ')[1].split(',')[0][2:4]
            rt = inst.split(' ')[1].split(',')[1]
            offset = inst.split(' ')[1].split(',')[0][0]
            offset = int(offset)
            if reg_Q[rs] == '':
                Qj = ''
                Vj = reg[rs]
            else:
                Qj = reg_Q[rs]
                Vj = 0
            if reg_d_Q[rt] == '':
                Qk = ''
                Vk = reg_d[rt]
            else:
                Qk = reg_d_Q[rt]
                Vk = 0
            store_rs[sd_rs] = {'Op': 'S.D', 'Qj': Qj, 'Qk': Qk, 'Vj': Vj, 'Vk': Vk, 'A': offset, 'Busy': 1}
            pc += 1
    elif op == 'MUL.D':
        m_rs = mult_can_issue()
        if m_rs != '':
            rd = inst.split(' ')[1].split(',')[0]
            rs = inst.split(' ')[1].split(',')[1]
            rt = inst.split(' ')[1].split(',')[2]
            if reg_d_Q[rs] == '':
                Qj = ''
                Vj = reg_d[rs]
            else:
                Qj = reg_d_Q[rs]
                Vj = 0
            if reg_d_Q[rt] == '':
                Qk = ''
                Vk = reg_d[rt]
            else:
                Qk = reg_d_Q[rt]
                Vk = 0
            reg_d_Q[rd] = m_rs
            mult_rs[m_rs] = {'Op': 'S.D', 'Qj': Qj, 'Qk': Qk, 'Vj': Vj, 'Vk': Vk, 'A': 0, 'Busy': 1}
            pc += 1
    elif op == 'DADDUI':
        a_rs = add_can_issue()
        if a_rs != '':
            rd = inst.split(' ')[1].split(',')[0]
            rs = inst.split(' ')[1].split(',')[1]
            imm = inst.split(' ')[1].split(',')[2][1:]
            imm = int(imm)
            if reg_Q[rs] == '':
                Qj = ''
                Vj = reg[rs]
            else:
                Qj = reg_Q[rs]
                Vj = 0
            reg_Q[rd] = a_rs
            add_rs[a_rs] = {'Op': 'S.D', 'Qj': Qj, 'Qk': '', 'Vj': Vj, 'Vk': 0, 'A': imm, 'Busy': 1}
            pc += 1
    else:
        if reg_Q['R1'] == '':
            if reg['R1'] != reg['R2']:
                pc = 0
            else:
                pc = -1
    # 执行和写回
    exe_write()

    print(pc, clock)
    print(reg_Q)
    print(reg)
    print(reg_d_Q)
    print(reg_d)
    # if(clock == 9): break
    clock += 1
# 用于所有指令发射完成后，将剩余在功能部件的指令执行完
while 1:
    exe_write()
    clock += 1
    if clock > 100:
        break
print(ram[0:81])
