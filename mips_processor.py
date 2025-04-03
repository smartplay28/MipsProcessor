import math

z = "0"*32
Register = {0:z}

input = ['00100000000011000001000000000001',
        '00100000000011010000000001111011',
        '10101101100011010000000000000000',
        '10001101100010000000000000000000',
        '00100000000010010000000000000000',
        '00100000000100000000000000001010',
        '00010001000000000000000000001000',
        '00000001001100000000000000011000',
        '00000000000000000100100000010010',
        '00000001000100000000000000011010',
        '00000000000000000101000000010000',
        '00000001001010100100100000100000',
        '00000001000100000000000000011010',
        '00000000000000000100000000010010',
        '00001000000000000000000000000110',
        '00100000000011100001000000000010',
        '10101101110010010000000000000000',
        '00100000000000100000000000001010',
        '00000000000000000000000000001100']

Instruction_Memory = [""]*(4096)    #Size = 0x00001000
index = 0
for i in range(len(input)):
  Ins_4 = input[i][0:8]
  Ins_3 = input[i][8:16]
  Ins_2 = input[i][16:24]
  Ins_1 = input[i][24:32]
  Instruction_Memory[index] = Ins_1
  index += 1
  Instruction_Memory[index] = Ins_2
  index += 1
  Instruction_Memory[index] = Ins_3
  index += 1
  Instruction_Memory[index] = Ins_4
  index += 1 

Data_Memory = [""]*(16383)    #Size = 0x00003fff


def bin_to_dec(bin_str):
  if(len(bin_str) == 0):
    return 0
  #print(f'The binary string is {bin_str} and length is {len(bin_str)}')
  sum = 0
  for i in range(len(bin_str) - 1, 0, -1):
    sum += int(bin_str[i]) * (2**(len(bin_str) - i - 1))
  sum -= int(bin_str[0]) * (2**(len(bin_str) - 1))
  return sum


def dec_to_bin(n, bits):
  if (n == 0):
    s = "0" * bits
    return s
  else:
    digits = math.log(abs(n), 2)
    digits = math.floor(digits + 1)
    s = ""
    if (n > 0):
      s = "0" * (bits - digits)
      s += format(n, 'b')
    else:
      s = "1" * (bits - digits)
      temp = format((2**digits - abs(n)), 'b')
      if (len(temp) < digits):
        temp = "0" * (digits - len(temp)) + temp
      s += temp
    return s


class PC:

  def __init__(self):
    self.PC = ""

  def update_PC(self, value):
    self.PC = value

  def call_IM(self):
    im.update_IM()
    im.call_ID()


class IM:

  def __init__(self):
    self.instr = ""

  def update_IM(self):
    self.instr = Instruction_Memory[bin_to_dec(pc.PC)+3] + Instruction_Memory[bin_to_dec(pc.PC)+2] + Instruction_Memory[bin_to_dec(pc.PC)+1] + Instruction_Memory[bin_to_dec(pc.PC)]
    print(f'Instruction = {self.instr}')

  def call_ID(self):
    id.update_ID()
    id.call_RegFile()


class Control_Unit:

  def __init__(self):
    self.RegWrite = ""
    self.ALUSrc = ""
    self.MemtoReg = ""
    self.RegDst = ""
    self.Branch = ""
    self.MemWrite = ""
    self.Write_Special_Purpose = ""
    self.ALUOp = ""
    self.ALUControl = ""

  def update_Control_Unit(self, op, funct):

    if (op == "000000"):  # R Format
      self.RegWrite = 1
      self.ALUSrc = 0
      self.MemtoReg = 0
      self.RegDst = 1
      self.Branch = 0
      self.MemWrite = 0
      self.ALUOp = "10"
    elif (op == "001000"):  # addi
      self.RegWrite = 1
      self.ALUSrc = 1
      self.MemtoReg = 0
      self.RegDst = 0
      self.Branch = 0
      self.MemWrite = 0
      self.ALUOp = "00"
    elif (op == "100011"):  # lw
      self.RegWrite = 1
      self.ALUSrc = 1
      self.MemtoReg = 1
      self.RegDst = 0
      self.Branch = 0
      self.MemWrite = 0
      self.ALUOp = "00"
    elif (op == "101011"):  # sw
      self.RegWrite = 0
      self.ALUSrc = 1
      self.MemtoReg = ""
      self.RegDst = ""
      self.Branch = 0
      self.MemWrite = 1
      self.ALUOp = "00"
    elif (op == "000100" or op == "000101"):  # beq and bne
      self.RegWrite = 0
      self.ALUSrc = 0
      self.MemtoReg = ""
      self.RegDst = ""
      self.Branch = 1
      self.MemWrite = 0
      self.ALUOp = "01"

    if (self.ALUOp == "00" and (funct == "")):
      self.ALUControl = "010"
    elif (self.ALUOp == "01" and (funct == "")):
      self.ALUControl = "110"
    else:
      if (funct == "100000"):  # add
        self.ALUControl = "010"
        self.Write_Special_Purpose = 0
      elif (funct == "100010"):  # sub
        self.ALUControl = "110"
        self.Write_Special_Purpose = 0
      elif(funct == "101010"): # slt
        self.ALUControl = "111"
        self.Write_Special_Purpose = 0
      elif (funct == "100100"):  # and
        self.ALUControl = "000"
        self.Write_Special_Purpose = 0
      # elif (funct == "100101"):  # or
      #   self.ALUControl = "001"
      #   self.Write_Special_Purpose = 0
      elif (funct == "011000"):  # mult
        self.ALUControl = "100"
        self.Write_Special_Purpose = 1
      elif (funct == "011010"):  # div
        self.ALUControl = "101"
        self.Write_Special_Purpose = 1
      elif (funct == "010000"):  # mfhi
        self.ALUControl = "011"
        self.Write_Special_Purpose = 0
      elif (funct == "010010"):  # mflo
        self.ALUControl = "001"
        self.Write_Special_Purpose = 0
    print(f'\nControl Signals for the current instruction ->')
    print(f'RegWrite = {self.RegWrite}, ALUSrc = {self.ALUSrc}, MemtoReg = {self.MemtoReg}, RegDst = {self.RegDst}, Branch = {self.Branch}, MemWrite = {self.MemWrite}, ALUControl = {self.ALUControl}, Write_Special_Purpose = {self.Write_Special_Purpose}')


class ID:

  def __init__(self):
    self.op = ""
    self.rs = ""
    self.rt = ""
    self.rd = ""
    self.sign_extended = ""
    self.shamt = ""
    self.funct = ""

  def update_ID(self):
    self.op = im.instr[0:6]
    if (self.op == "000000"): # R format
      if(im.instr[:28] == "0"*28 and im.instr[28:] == "1100" and Register[2] == dec_to_bin(10, 32)): # syscall
        done = "HALT"
        print(f'\n{done}')
        print('\nx-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
        print(f'\nThe answer is stored in Memory Location {"0x0000" + hex(int(Register[14], 2))[2:]} (i.e {int(Register[14], 2)})')
        print(f'M[{int(Register[14], 2)}] = {bin_to_dec(Data_Memory[4098])}')
        exit()
      else:
        self.rs = im.instr[6:11]
        self.rt = im.instr[11:16]
        self.rd = im.instr[16:21]
        self.shamt = im.instr[21:26]
        self.funct = im.instr[26:]
        self.sign_extended = ""
        print(f'\nDecoding Instruction ->')
        print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rt, 2)} rd = {int(self.rd, 2)} funct = {int(self.funct, 2)} shamt = {int(self.shamt, 2)} sign_extended = {self.sign_extended}')
        control.update_Control_Unit(self.op, self.funct)

    if (self.op == "001000"): # addi
      self.rs = im.instr[6:11]
      self.rt = ""
      self.rd = im.instr[11:16]
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[16] * 16 + im.instr[16:]
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rd, 2)} rd = {self.rt} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      control.update_Control_Unit(self.op, self.funct)

    if (self.op == "100011"): # lw
      self.rs = im.instr[6:11]
      self.rt = ""
      self.rd = im.instr[11:16]
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[16] * 16 + im.instr[16:]
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rd, 2)} rd = {self.rt} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      control.update_Control_Unit(self.op, self.funct)

    if (self.op == "101011"): # sw
      self.rs = im.instr[6:11]
      self.rt = im.instr[11:16]
      self.rd = ""
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[16] * 16 + im.instr[16:]
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rt, 2)} rd = {self.rd} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      control.update_Control_Unit(self.op, self.funct)

    if (self.op == "000100"): # beq
      self.rs = im.instr[6:11]
      self.rt = im.instr[11:16]
      self.rd = ""
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[16] * 16 + im.instr[16:]
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rt, 2)} rd = {self.rd} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      control.update_Control_Unit(self.op, self.funct)

    if (self.op == "000101"): # bne
      self.rs = im.instr[6:11]
      self.rt = im.instr[11:16]
      self.rd = ""
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[16] * 16 + im.instr[16:]
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {int(self.rs, 2)} rt = {int(self.rt, 2)} rd = {self.rd} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      control.update_Control_Unit(self.op, self.funct)

    if (self.op == "000010"): # j
      self.rs = ""
      self.rt = ""
      self.rd = ""
      self.funct = ""
      self.shamt = ""
      self.sign_extended = im.instr[6:]
      self.sign_extended += "0" * 2
      zero = "0" * 4
      self.sign_extended = zero + self.sign_extended
      print(f"\nRegister's Values -> ", end = "")
      for key, value in Register.items():
          print(f'({key} -> {bin_to_dec(value)})', end = " ") 
      print('\n',end = "")
      print(f'\nDecoding Instruction ->')
      print(f'op = {self.op} rs = {self.rs} rt = {self.rt} rd = {self.rt} funct = {self.shamt} shamt = {self.shamt} sign_extended = {bin_to_dec(self.sign_extended)}')
      print(f'\nJumping and PC is updated to {bin_to_dec(self.sign_extended)}')
      print('\n', end = "")
      print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
      print(f'PC = {bin_to_dec(self.sign_extended)}')
      print(f'\nFetching Instruction ->')
      pc.update_PC(self.sign_extended)

      pc.call_IM()




  def call_RegFile(self):
    reg_file.update_REG_FILE()
    reg_file.read()
    reg_file.call_ALU()


class REG_FILE:

  def __init__(self):
    self.A1 = ""
    self.A2 = ""
    self.A3 = ""
    self.hi = ""
    self.lo = ""
    self.RD_hi = ""
    self.RD_lo = ""
    self.RD1 = ""
    self.RD2 = ""
    self.WD3 = ""

  def update_REG_FILE(self):
    self.A1 = id.rs
    self.A2 = id.rt
    self.A3 = id.rd
    print(f'\nGiving the corresponding addresses to the Register File ->')
    if(self.A1 != ""):
        print(f'A1 = {int(self.A1, 2)}', end = ", ")
    else:
        print(f'A1 = {self.A1}', end = ", ")
    if(self.A2 != ""):
        print(f'A2 = {int(self.A2, 2)}', end = ", ")
    else:
        print(f'A2 = {self.A2}', end = ", ")
    if(self.A3 != ""):
        print(f'A3 = {int(self.A3, 2)}')
    else:
        print(f'A3 = {self.A3}')

  def read(self):

    #print(f'Register index is {self.A1}')
    #print(f'Register value is {Register[0]}')
    if(self.A1 != ""):
        #print(f'########################{}')
        self.RD1 = Register[int(self.A1, 2)]
    if (self.A2 != ""):
      #print(self.A2)
      #if(16 in Register):
        #print(Register[16])
      self.RD2 = Register[int(self.A2, 2)]
    if (self.hi != "" and self.lo != ""):
      self.RD_hi = self.hi
      self.RD_lo = self.lo

    print(f"\nRegister's Values -> ")
    for key, value in Register.items():
        print(f'({key} -> {bin_to_dec(value)})', end = " ") 
    print('\n',end = "")
    print(f'\nValues read from the register file and stored in corresponding read ports ->')
    if(self.RD1 != ""):
        print(f'RD1 = {bin_to_dec(self.RD1)}', end = ", ")
    else:
        print(f'RD1 = {self.RD1}', end = ", ")
    if(self.RD2 != ""):
        print(f'RD2 = {bin_to_dec(self.RD2)}', end = ", ")
    else:
        print(f'RD2 = {self.RD2}', end = ", ")
    if(self.RD_hi != ""):
        print(f'RD_hi = {bin_to_dec(self.RD_hi)}', end = ", ")
    else:
        print(f'RD_hi = {self.RD_hi}', end = ", ")
    if(self.RD_lo != ""):
        print(f'RD_lo = {bin_to_dec(self.RD_lo)}')
    else:
        print(f'RD_lo = {self.RD_lo}')

  def call_ALU(self):
    alu.update_ALU()
    alu.calculate_ALU()
    alu.call_Mem()




class ALU:

  def __init__(self):
    self.Src_hi = ""
    self.Src_lo = ""
    self.SrcA = ""
    self.SrcB = ""
    self.ALUResult = ""
    self.hiResult = ""
    self.loResult = ""

  def update_ALU(self):
    self.Src_hi = reg_file.RD_hi
    self.Src_lo = reg_file.RD_lo
    self.SrcA = reg_file.RD1
    if (control.ALUSrc):
      self.SrcB = id.sign_extended
    else:
      self.SrcB = reg_file.RD2
    print(f'\nGiving values to ALU Sources according to the control signals->')
    if(self.SrcA != ""):
        print(f'SrcA = {bin_to_dec(self.SrcA)}', end = ", ")
    else:
        print(f'SrcA = {self.SrcA}', end = ", ")
    if(self.SrcB != ""):
        print(f'SrcB = {bin_to_dec(self.SrcB)}', end = ", ")
    else:
        print(f'SrcB = {self.SrcB}', end = ", ")
    if(self.Src_hi != ""):
        print(f'Src_hi = {bin_to_dec(self.Src_hi)}', end = ", ")
    else:
        print(f'Src_hi = {self.Src_hi}', end = ", ")
    if(self.Src_lo != ""):
        print(f'Src_lo = {bin_to_dec(self.Src_lo)}')
    else:
        print(f'Src_lo = {self.Src_lo}')


  def calculate_ALU(self):
    if (control.ALUControl == "010"):
      self.ALUResult = bin_to_dec(self.SrcA) + bin_to_dec(self.SrcB)
      #print('\n')
      #print(f'#############{bin_to_dec(self.SrcA) + bin_to_dec(self.SrcB)}############')
      self.ALUResult = dec_to_bin(self.ALUResult, 32)
      self.hiResult = ""
      self.loResult = ""

    elif (control.ALUControl == "110"):
      self.ALUResult = bin_to_dec(self.SrcA) - bin_to_dec(self.SrcB)
      self.ALUResult = dec_to_bin(self.ALUResult, 32)
      self.hiResult = ""
      self.loResult = ""

    elif (control.ALUControl == "000"):
      self.ALUResult = bin_to_dec(self.SrcA) & bin_to_dec(self.SrcB)
      self.ALUResult = dec_to_bin(self.ALUResult, 32)
      self.hiResult = ""
      self.loResult = ""

    # if (control.ALUControl == "001"):
    #   self.ALUResult = bin_to_dec(self.SrcA) | bin_to_dec(self.SrcB)
    #   self.ALUResult = dec_to_bin(self.ALUResult, 32)
    #   self.hiResult = ""
    #   self.loResult = ""

    elif(control.ALUControl == "111"):
      self.ALUResult = bin_to_dec(self.SrcA) - bin_to_dec(self.SrcB)
      if(self.ALUResult < 0):
        self.ALUResult = "1"*32
      else:
        self.ALUResult = "0"*32
      self.hiResult = ""
      self.loResult = ""

    elif (control.ALUControl == "100"):
      self.hiResult = bin_to_dec(self.SrcA) * bin_to_dec(self.SrcB)
      self.hiResult = dec_to_bin(self.hiResult, 64)
      self.loResult = self.hiResult[32:]
      self.hiResult = self.hiResult[0:32]
      self.ALUResult = ""

    elif (control.ALUControl == "101"):
      self.loResult = bin_to_dec(self.SrcA) // bin_to_dec(self.SrcB)
      self.hiResult = bin_to_dec(self.SrcA) % bin_to_dec(self.SrcB)
      self.hiResult = dec_to_bin(self.hiResult, 32)
      self.loResult = dec_to_bin(self.loResult, 32)
      self.ALUResult = ""

    elif (control.ALUControl == "011"):
      self.ALUResult = self.Src_hi
      self.hiResult = ""
      self.loResult = ""

    elif (control.ALUControl == "001"):
      self.ALUResult = self.Src_lo
      self.hiResult = ""
      self.loResult = ""

    print(f'\nThe result generated from the ALU ->')
    if(self.ALUResult != ""):
        print(f'ALUResult = {bin_to_dec(self.ALUResult)}', end = ", ")
    else:
        print(f'ALUResult = {self.ALUResult}', end = ", ")
    if(self.hiResult != ""):
        print(f'hiResult = {bin_to_dec(self.hiResult)}', end = ", ")
    else:
        print(f'hiResult = {self.hiResult}', end = ", ")
    if(self.loResult != ""):
        print(f'loResult = {bin_to_dec(self.loResult)}')
    else:
        print(f'loResult = {self.loResult}')



  def call_Mem(self):
    mem.update_Mem()
    mem.read_Mem()
    mem.call_WB()


class Mem:

  def __init__(self):
    self.A = ""
    self.WD = ""
    self.RD = ""

  def update_Mem(self):
    self.A = alu.ALUResult
    if(id.op == "101011"):
        self.WD = reg_file.RD2
    else:
        self.WD = ""

    print(f'\nPassing the ALU results to the Data Memory Register ->')

    if(self.A != ""):
        print(f'A = {bin_to_dec(self.A)}', end = ", ")
    else:
        print(f'A = {self.A}', end = ", ")
    if(self.WD != ""):
        print(f'WD = {bin_to_dec(self.WD)}')
    else:
        print(f'WD = {self.WD}')

  def read_Mem(self):
    if (self.A == "0"*32 and control.Branch):
      id.sign_extended = id.sign_extended[2:] + "0" * 2
      pc_temp = bin_to_dec(pc.PC) + 4
      pc_temp = pc_temp + bin_to_dec(id.sign_extended)
      print('\n', end = "")
      print(f'Branching and PC is updated to {pc_temp}')
      print(f'\n', end = "")
      print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
      print(f'PC = {pc_temp}')
      print(f'\nFetching Instruction ->')
      pc.update_PC(dec_to_bin(pc_temp, 32))
      pc.call_IM()
    else:
      pc_temp = bin_to_dec(pc.PC) + 4
      pc.update_PC(dec_to_bin(pc_temp, 32))

    if (control.MemWrite):
      Data_Memory[int(self.A, 2)] = self.WD
      self.RD = ""
    else:
      #if (Instruction_Memory[bin_to_dec(self.A)] is not None):
      if(id.op == "100011"):
        self.RD = Data_Memory[int(self.A, 2)]
      else:
        self.RD = ""
      # Call write back
    print(f'\nData read from Data Memory ->')
    if(self.RD != ""):
        print(f'RD = {bin_to_dec(self.RD)}')
    else:
        print(f'RD = {self.RD}')



  def call_WB(self):
    wb.update_WB()
    wb.write_WB()
    wb.call_PC()


class Write_Back:

  def __init__(self):
    self.write_A3 = ""
    self.write_hi = ""
    self.write_lo = ""

  def update_WB(self):
    self.write_hi = alu.hiResult
    self.write_lo = alu.loResult
    if (control.MemtoReg):
      self.write_A3 = mem.RD
    else:
      self.write_A3 = alu.ALUResult

    print(f'\nData to be written back to the Register File ->')

    if(self.write_A3 != ""):
        print(f'write_A3 = {bin_to_dec(self.write_A3)}', end = ", ")
    else:
        print(f'write_A3 = {self.write_A3}', end = ", ")
    if(self.write_hi != ""):
        print(f'write_hi = {bin_to_dec(self.write_hi)}', end = ", ")
    else:
        print(f'write_hi = {self.write_hi}', end = ", ")
    if(self.write_lo != ""):
        print(f'write_lo = {bin_to_dec(self.write_lo)}')
    else:
        print(f'write_lo = {self.write_lo}')

  def write_WB(self):
    if (control.Write_Special_Purpose):
      reg_file.hi = self.write_hi
      reg_file.lo = self.write_lo
      print(f'\nWriting data to correspoding register ->')
      print(f'Writing {bin_to_dec(self.write_hi)} -> hi and {bin_to_dec(self.write_lo)} -> lo')
    if (control.RegWrite):
      print(f'\nWriting data to correspoding register ->')
      print(f'Writing {bin_to_dec(wb.write_A3)} -> {int(reg_file.A3, 2)}')
      Register[int(reg_file.A3, 2)] = wb.write_A3



  def call_PC(self):
    print('\n', end = "")
    print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
    print(f'PC = {bin_to_dec(pc.PC)}')
    print(f'\nFetching Instruction -> ')
    pc.call_IM()



pc = PC()
im = IM()
id = ID()
control = Control_Unit()
reg_file = REG_FILE()
alu = ALU()
wb = Write_Back()
mem = Mem()
print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
print(f'PC = {0}')
pc.update_PC(dec_to_bin(0, 32))
pc.call_IM()