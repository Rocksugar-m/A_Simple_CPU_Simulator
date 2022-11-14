import copy

#
# Loop:	fld 	f0,0(x1)	            //f0=array element
#           	fadd.d 	f4,f0,f2	    //add scalar in f2
# 	            fsd 		f4,0(x1) 	//store result
# 	            addi 		x1,x1,8 	//decrement pointer
# 					                    //8 bytes (per DW)
#           	bne 		x1,x2,Loop	//branch x1 != x2

insts = ['fld f0,0(x1)', 'fadd.d f4,f0,f2', 'fsd f4,0(x1)', 'addi x1,x1,8', 'bne x1,x2,0']
splitinsts = []
unruollinsts = []
relyreg = []
usereg = []
reguse = []
instsall = []
for i in range(16):
    reguse.append(-1)


def unroll(insts):
    for i in range(len(insts)):  # 分割指令，取出指令用到的寄存器
        temp = [insts[i].split()[0], insts[i].split()[1].split(',')[0], insts[i].split()[1].split(',')[1]]
        if len(insts[i].split()[1].split(',')) > 2:
            temp.append(insts[i].split()[1].split(',')[2])
        splitinsts.append(temp.copy())

    for i in range(len(splitinsts)):  # 有依赖关系的寄存器，即在展开的时候需要换名字的寄存器
        if (splitinsts[i][0] != 'fsd') & (splitinsts[i][0] != 'bne'):
            relyreg.append(splitinsts[i][1])
        else:
            relyreg.append(0)
    for i in range(len(splitinsts)):  # 记录已经使用的寄存器
        for j in range(1, len(splitinsts[i])):
            if splitinsts[i][j].find('f') >= 0:
                reguse[int(splitinsts[i][j].split('f')[1])] = 0

    for i in range(len(splitinsts) - 1):  # 找到自增量
        if (splitinsts[i][0] == 'addi') & (splitinsts[i + 1][0] == 'bne'):
            addval = int(splitinsts[i][3])
            reg = splitinsts[i][1]

    instsall.append(copy.deepcopy(splitinsts))
    instsall.append(copy.deepcopy(splitinsts))
    instsall.append(copy.deepcopy(splitinsts))
    instsall.append(copy.deepcopy(splitinsts))
    for i in range(1, len(instsall)):
        for j in range(len(instsall[i]) - 2):
            for k in range(1, len(instsall[i][j])):
                if instsall[i][j][k] in relyreg:  # 主要展开的步骤之寄存器换名
                    if reguse[int(instsall[i][j][k].split('f')[1])] == 0:
                        index1 = reguse.index(-1)
                        reguse[index1] = 0
                        reguse[int(instsall[i][j][k].split('f')[1])] = index1
                    else:
                        index1 = reguse[int(instsall[i][j][k].split('f')[1])]
                    instsall[i][j][k] = 'f' + str(index1)
                    relyreg.append(instsall[i][j][k])

                if instsall[i][j][k].find(reg) >= 0:  # 主要展开的步骤之改变偏移地址
                    instsall[i][j][k] = str(int(instsall[i][j][k].split('(')[0]) + addval * i) + '(' + reg + ')'
        for i in range(len(reguse)):  # 记录使用过的寄存器
            if reguse[i] > 0:
                reguse[i] = 0
    for i in range(len(instsall) - 1):  # 去除循环展开后前面三段的后两条循环判断指令
        del instsall[i][len(instsall[i]) - 1]
        del instsall[i][len(instsall[i]) - 1]
    result = []
    for i in range(len(instsall[0])):  # 初步调度指令，将所有同操作的指令放在一起
        for j in range(len(instsall)):
            result.append(instsall[j][i])
    result.append(instsall[len(instsall) - 1][len(instsall[len(instsall) - 1]) - 2])
    result.append(instsall[len(instsall) - 1][len(instsall[len(instsall) - 1]) - 1])

    temp = result[len(result) - 4]  # 调整最后的指令顺序
    result[len(result) - 4] = result[len(result) - 2]
    result[len(result) - 4][3] = str(addval * 4)
    result[len(result) - 2] = result[len(result) - 1]
    result[len(result) - 1] = result[len(result) - 3]
    result[len(result) - 1][2] = str(int(result[len(result) - 1][2].split('(')[0]) - addval * 4) + '(' + reg + ')'
    temp[2] = str(int(temp[2].split('(')[0]) - addval * 4) + '(' + reg + ')'
    result[len(result) - 3] = temp
    print("循环展开前指令为：")
    print(insts)
    print("循环展开后指令为：")
    resultinst = []
    for i in range(len(result)):  # 将操作码，操作数合成完整的指令
        if len(result[i]) == 3:
            resultinst.append(result[i][0] + ' ' + result[i][1] + ',' + result[i][2])
        else:
            resultinst.append(result[i][0] + ' ' + result[i][1] + ',' + result[i][2] + ',' + result[i][3])
        print(resultinst[i])


unroll(insts)
