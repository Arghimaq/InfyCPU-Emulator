import os
import time
import GPU_Computer as GPU
import sys


#Variables

#Data organization

Instruction_size = 3
ROM_SIZE = Instruction_size * 64
RAM_SIZE = 1028

RAM = [0] * RAM_SIZE
ROM = [0] * ROM_SIZE

#Video Variables

color = 0

#Registers

Register_A = 0
Register_B = 0
Register_C = 0

#Malicious

Accumulator = 0

PC = 0

#Flags or Booleans

Jump_Flag = False
Zero_Flag = False
Input_Flag = False
Cmp_Flag = False

Machine_State = True

#Define Retrive ROM.txt

def get_rom():
	global ROM
	with open('ROM.txt', 'r') as f:
		instructions = f.read().split()
		print(f"Retrieved ROM: {instructions}. Converting to intergers")
		i = 0
		for instruction in instructions:
			try:
				instructions[i] = int(instruction)
			except ValueError:
				instructions[i] = str(instruction)
			i+=1
		print(f"Successfully converted to intergers: {instructions}")
		if len(instructions) == ROM_SIZE:
			for i in range(len(ROM)):
				ROM[i] = instructions[i]
		else:
			print("Error: ROM exceeds ROM size. Erasing ROM.")
			ROM = [0] * ROM_SIZE
		

#Define get bits

def get():
	global PC
	return ROM[PC], ROM[PC+1], ROM[PC+2]


#Decode and Run

def run():
	#Globals
	global Accumulator
	global Register_A
	global Register_B
	global Register_C
	global color
	global Machine_State
	global PC
	global Zero_Flag
	global Input_Flag
	global Cmp_Flag
	
		#Unpack
	opcode, operand1, operand2 = get()
	
		#ALU----------------------------------------------------------
	
	
	if opcode == 1:		#Addition
		Accumulator = operand1 + operand2
		if Accumulator == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
	
	elif opcode == 2:		#Subtract
		Accumulator = operand1 - operand2
		if Accumulator == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
			
	elif opcode == 3:		#Division
		Accumulator = operand1 / operand2
		if Accumulator == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
			
	elif opcode == 4:		#Multiplication
		Accumulator = operand1 * operand2
		if Accumulator == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
	
	elif opcode == 5:		#Compare if greater
		if operand1 > operand2:
			Cmp_Flag = True
		else:
			Cmp_Flag = False
	
	elif opcode == 6:		#Compare if lower
		if operand1 < operand2:
			Cmp_Flag = True
		else:
			Cmp_Flag = False
	
	elif opcode == 7:		#Compare if equal
		if operand1 == operand2:
			Cmp_Flag = True
		else:
			Cmp_Flag = False
		
			
		#Memory-------------------------------------------------------
	
	
	elif opcode == 10:	#Store operand1 at RAM address operand2
		RAM[operand2] = operand1
	
	elif opcode == 11:	#Store operand1 at register 0 = A, 1 = B, 2 = C
		if operand2 == 0:
			Register_A = operand1
		elif operand2 == 1:
			Register_B = operand1
		elif operand2 == 2:
			Register_C = operand1
	
	elif opcode == 12:		#Load Register operand1 at RAM address operand2
		if operand1 == 0:
			RAM[operand2] = Register_A
		elif operand1 == 1:
			RAM[operand2] = Register_B
		elif operand1 == 2:
			RAM[operand2] = Register_C
	
	elif opcode == 13:		#Store value from RAM address operand1 into register operand2
		if operand2 == 0:
			Register_A = RAM[operand1]
		elif operand2 == 1:
			Register_B = RAM[operand1]
		elif operand2 == 2:
			Register_C = RAM[operand1]
	
	elif opcode == 14:		#Store Accumulator value into RAM address operand1. If operand2 = 1, do opposite
		if operand2 == 0:
			RAM[operand1] = Accumulator
		else:
			Accumulator = RAM[operand1]
	
	elif opcode == 15:		#Store value from RAM address operand1 into ROM address operand2
		ROM[operand2] = RAM[operand1]
		
		
		#Memory-Math------------------------------------------
		
		
	elif opcode == 30:		#Add Register operand1 and operand2
		if operand1 == 0:
			Accumulator = Register_A + Register_B
		elif operand1 == 1:
			Accumulator = Register_A + Register_C
		elif operand2 == 2:
			Accumulator = Register_B + Register_C
	
	elif opcode == 31:		#Subtract Register operand1 and operand2
		if operand2 == 0:
			if operand1 == 0:
				Accumulator = Register_A - Register_B
			elif operand1 == 1:
				Accumulator = Register_A - Register_C
			elif operand2 == 2:
				Accumulator = Register_B - Register_C
		else:
			if operand1 == 0:
				Accumulator = Register_B - Register_A
			elif operand1 == 1:
				Accumulator = Register_C - Register_A
			elif operand2 == 2:
				Accumulator = Register_C - Register_B
	
	elif opcode == 32:		#Multiply Register operand1 and operand2
		if operand1 == 0:
			Accumulator = Register_A * Register_B
		elif operand1 == 1:
			Accumulator = Register_A * Register_C
		elif operand2 == 2:
			Accumulator = Register_B * Register_C
	
	elif opcode == 33:		#Subtract Register operand1 and operand2
		if operand2 == 0:
			if operand1 == 0:
				Accumulator = Register_A / Register_B
			elif operand1 == 1:
				Accumulator = Register_A / Register_C
			elif operand2 == 2:
				Accumulator = Register_B / Register_C
		else:
			if operand1 == 0:
				Accumulator = Register_B / Register_A
			elif operand1 == 1:
				Accumulator = Register_C / Register_A
			elif operand2 == 2:
				Accumulator = Register_C / Register_B
	
	
		#Jump-related------------------------------------------------
		
		
	elif opcode == 20:		#Jump into ROM address operand1
		Jump_Flag = True
		PC = operand1
		print("Jumped!")
		
	elif opcode == 21:		#Jump into ROM address operand1 if Zero Flag is true. if operand2 = 1, do opposite
		if operand2 == 0:
			if Zero_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
				Zero_Flag = False
		else:
			if not Zero_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
	
	elif opcode == 22:		#Jump into ROM address operand1 if Input Flag is true. if operand2 = 1, inverse
		if operand2 == 0:
			if Input_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
				Input_Flag = False
		else:
			if not Input_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
	
	elif opcode == 23:		#Jump into ROM address operand1 in Compare Flag is true. if operand2 = 1, inverse
		if operand2 == 0:
			if Cmp_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
				Input_Flag = False
		else:
			if not Cmp_Flag:
				Jump_Flag = True
				PC = operand1
				print("Jumped!")
		
		#Input-Output-----------------------------------------------
		
		
	elif opcode == 40:		#Listen for input
		key = GPU.listen()
		if key is not None:
			Input_Flag = True
			Accumulator = key
			print("Input received")
		
		
				
		#Malicious--------------------------------------------------
	
	elif opcode == 999:
		Machine_State = False
	
	elif opcode == 111:
		print(str(operand1))	#Warning: might be inaccurate
		
		
		#Video-------------------------------------------------------
		
	elif opcode == 200:		#Draw. operand1 = x, operand2 = y
		GPU.draw(operand1,operand2,color)
	
	elif opcode == 201:		#Erase
		GPU.erase(operand1,operand2)
	
	elif opcode == 202:		#Change color. operand1 = color
		color = operand1
	
#Get ROM.txt
	
get_rom()

os.system('cls')
print("Running...")


def tick():
	global PC
	global Instruction_size
	global Jump_Flag
	global Input_Flag
	run()
	if Jump_Flag == False:
		PC+=Instruction_size
	else:
		Jump_Flag = False
	
def cycle():
	tick()
	
GPU.initialize()
while Machine_State:
	cycle()
	if GPU.check_quit():
		break
	GPU.update_display()

#Final Results
os.system('cls')

print(f"""
	Final Results:
	Accumulator: {Accumulator}
	
	Registers:
	A: {Register_A}
	B: {Register_B}
	C: {Register_C}
	
	RAM:
	{RAM}
	
	
	ROM:
	{ROM}
	
""")
