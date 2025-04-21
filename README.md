# MIPS Processor Simulator

A Python-based simulator that models the execution of MIPS assembly instructions through a pipelined architecture.

## Overview

This project implements a MIPS processor simulator that can parse, decode, and execute MIPS instructions. The simulator follows a pipeline architecture consisting of the following stages:
- Instruction Fetch (IF)
- Instruction Decode (ID)
- Execute (EX)
- Memory Access (MEM)
- Write Back (WB)

The simulator provides detailed output at each stage of the pipeline, making it a useful educational tool for understanding processor architecture and MIPS instruction execution.

## Features

- Supports key MIPS instructions including:
  - R-format instructions (add, sub, and, slt, mult, div)
  - Memory operations (lw, sw)
  - Immediate operations (addi)
  - Branch operations (beq, bne)
  - Jump operations (j)
  - System calls (syscall)
- Pipeline simulation with detailed output for each stage
- Register file and memory simulation
- Binary to decimal and decimal to binary conversion utilities
- Control unit with signals for ALU operations, memory access, branching, etc.

## How it Works

The simulator models the following components:
- Program Counter (PC)
- Instruction Memory (IM)
- Instruction Decoder (ID)
- Control Unit
- Register File
- Arithmetic Logic Unit (ALU)
- Data Memory
- Write Back Logic

Each instruction passes through these components in sequence, with detailed output showing the state of registers, control signals, and computed values at each step.

## Usage

1. Define your MIPS assembly instructions as binary strings in the `input` list.
2. Run the script.
3. The simulator will execute each instruction and display detailed information about each step of the process.
4. When a syscall instruction with value 10 in register $v0 is encountered, the program halts and displays the final result.

## Example Output

The simulator provides detailed output for each stage of the pipeline execution:

```
PC = 0
Fetching Instruction ->
Instruction = 00100000000011000001000000000001

Decoding Instruction ->
op = 001000 rs = 0 rt = 12 rd =  funct =  shamt =  sign_extended = 1

Control Signals for the current instruction ->
RegWrite = 1, ALUSrc = 1, MemtoReg = 0, RegDst = 0, Branch = 0, MemWrite = 0, ALUControl = 010, Write_Special_Purpose = 

Giving the corresponding addresses to the Register File ->
A1 = 0, A2 = , A3 = 

Register's Values -> 
(0 -> 0) 

Values read from the register file and stored in corresponding read ports ->
RD1 = 0, RD2 = , RD_hi = , RD_lo = 

Giving values to ALU Sources according to the control signals->
SrcA = 0, SrcB = 1, Src_hi = , Src_lo = 

The result generated from the ALU ->
ALUResult = 1, hiResult = , loResult = 

Passing the ALU results to the Data Memory Register ->
A = 1, WD = 

Data read from Data Memory ->
RD = 

Data to be written back to the Register File ->
write_A3 = 1, write_hi = , write_lo = 

Writing data to correspoding register ->
Writing 1 -> 12

x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
PC = 4
Fetching Instruction ->
...
```

## Requirements

- Python 3.x
- Standard Python libraries (math)
