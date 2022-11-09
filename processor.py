def fetch_instructions(fileName):
    """
    :param fileName: in what file the instructions are stored.
    :return: a list of instructions
    """
    with open(fileName) as f:
        instruction_list = f.readlines()
        for i in range(len(instruction_list)):
            instruction_list[i] = instruction_list[i].strip("\n")
    return instruction_list


def malloc_memory():
    """
    We don't need to initialize a very big memory in this case.
    :return:
    """
    global Memory, BLOCK_SIZE, Memory_SIZE
    print("Need to malloc a new memory block!")
    new_memory_block = [0] * BLOCK_SIZE
    Memory.extend(new_memory_block)
    Memory_SIZE += BLOCK_SIZE
    print("Successfully malloced.")
    return None


def sign_extend(bin_str):
    """
    :param bin_str: binary string
    :return: integer
    """
    if bin_str[0] == '0':
        result = int(bin_str, 2)
    else:
        result = int(bin_str, 2) - (1 << 16)
    return result


def lb(base, reg_index, offset):
    """
    load Byte

    :param base: base register(rs) index
    :param reg_index: target register(rt) index
    :param offset: memory address offset
    :return:
    :raise IndexError: malloc memory when memory is out of bounds
    """
    reg_index = int(reg_index, 2)
    read_addr = regs[int(base, 2)] + sign_extend(offset)
    try:
        Memory[read_addr]
    except IndexError:
        malloc_memory()
    finally:
        regs[reg_index] = Memory[read_addr]
        print("Load word %d (Memory addr #%d) successfully into register $r%d."
              % (Memory[read_addr], read_addr, reg_index))
    return None


def sb(base, reg_index, offset):
    """
    store Byte

    :param base: base register(rs) index
    :param reg_index: read register(rt) index
    :param offset: memory address offset
    :return:
    :raise IndexError: malloc memory when memory is out of bounds
    """
    reg_index = int(reg_index, 2)
    write_addr = regs[int(base, 2)] + sign_extend(offset)
    try:
        Memory[write_addr]
    except IndexError:
        malloc_memory()
    finally:
        Memory[write_addr] = regs[reg_index]
        print("Store $r%d (%d) successfully into register Memory addr #%d."
              % (reg_index, regs[write_addr], write_addr))


def j(pc, target):
    """
    jump

    :param pc: current PC
    :param target: low 25-0 bits of target PC
    :return: target PC
    """
    pc = int(bin(pc & 0xf0000000)[0:4] + target, 2)
    return pc


def bgtz(pc, reg_index, offset):
    """
    Branch on greater than 0

    :param pc: current PC
    :param reg_index: the condition compared with 0
    :param offset: the offset of target PC from current PC
    :return: target PC
    """
    reg_index = int(reg_index, 2)
    if regs[reg_index] > 0:
        pc = pc + sign_extend(offset)
    else:
        pc += 1
    return pc


def addu(op1_index, op2_index, target):
    """
    unsigned add

    :param op1_index: rs index
    :param op2_index: rt index
    :param target: rd index
    :return:
    """
    target = int(target, 2)
    op1_index = int(op1_index, 2)
    op2_index = int(op2_index, 2)
    regs[target] = regs[op1_index] + regs[op2_index]
    return


def addiu(op1_index, target, imm):
    """
    unsigned immediate add

    :param op1_index: rs index
    :param target: rt index
    :param imm: signed immediate
    :return:
    """
    target = int(target, 2)
    op1_index = int(op1_index, 2)
    op2 = sign_extend(imm)
    regs[target] = regs[op1_index] + op2
    return


def run_processor(instruction_list):
    """
    run the processor
    :param instruction_list:
    :return:
    """
    global PC, regs, Memory, Memory_SIZE
    while True:
        inst = instruction_list[PC]
        PC += 1
        opcode = inst[0:6]
        rs = inst[6:11]
        rt = inst[11:16]
        rd = inst[16:21]
        sa = inst[21:26]
        function = inst[26:32]
        immediate = inst[16:32]
        offset = inst[16:32]
        jump_target = inst[6:32]

        # exe
        if opcode == '100000':
            lb(rs, rt, offset)
        elif opcode == '101000':
            sb(rs, rt, offset)
        elif opcode == '000000' and sa == '00000' and function == '100001':
            addu(rs, rt, rd)
        elif opcode == '001001':
            addiu(rs, rt, immediate)
        elif opcode == '000010':
            PC = j(PC-1, jump_target)
        elif opcode == '000111' and rt == '00000':
            PC = bgtz(PC-1, rs, offset)
        elif inst == '00000000000000000000000000000000':
            break
    return None


if __name__ == '__main__':
    PC = 0
    regs = [0] * 32
    BLOCK_SIZE = 2 ** 10
    # total 4GB and a block is 2B
    # if the processor need more memory, it will malloc.
    Memory = [0] * BLOCK_SIZE
    Memory_SIZE = BLOCK_SIZE
    # To verify the result
    Memory[0] = 1
    Memory[1] = 2
    Memory[2] = 10
    print("To verify the result, calculate addition from 1 to %d" % Memory[2])
    instructions = fetch_instructions("rom.txt")
    run_processor(instructions)
    assert Memory[3] == 55
    print("Result is %d, Successfully simulated!" % Memory[3])
    print("Memory_SIZE = %d" % Memory_SIZE)
