

instruction_list = {
	"add": 1,
	"sub": 2,
	"div": 3,
	"mul": 4,
	"cmpg": 5,
	"cmpl": 6,
	"cmpe": 7,
	
	"strram": 10,
	"strreg": 11,
	"ldregram": 12,
	"strramreg": 13,
	"stracmram": 14,
	"ram2rom": 15,
	
	"jmp": 20,
	"jz": 21,
	"jinp": 22,
	"jcmp": 23,
	
	"inp": 40,
	
	"hlt": 999,
	"print": 111,
	
	"draw": 200,
	"erase": 201,
	"clr": 202
}
DecompiledROM = []
CompiledROM = []

from tkinter import filedialog

file_path = filedialog.askopenfilename(
	title="Select ROM",
	defaultextension=".txt",
	filetypes=[("Text files", "*.txt")]
	
)

with open(file_path, 'r') as f:
    for line in f:
        # Remove comments beginning with #
        line = line.split(';', 1)[0].strip()

        # Add only the actual code
        DecompiledROM.extend(line.split())
		
def compile(instruction_size, rom_size):
	for instruction in DecompiledROM:
		compiled_instruction = str(instruction_list.get(instruction))
		if compiled_instruction == 'None':
			CompiledROM.append(str(instruction))
		else:
			CompiledROM.append(compiled_instruction)
	
	leftover_bits = instruction_size * rom_size - len(CompiledROM)
	for i in range(leftover_bits):
		CompiledROM.append('0')
	
	with open('ROM.txt', 'w') as f:
		for i in CompiledROM:
			f.write(i + '\n')
	
		
		
compile(3, 64)

print(DecompiledROM)
print(CompiledROM)
		
