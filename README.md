# InfyCPU-Emulator

InfyCPU Emulator is a emulator of an experimental CPU. It has no bit constraints.

# How to use it

1. *Write your program* in the CPU's assembly language. Save it as a .txt file. (Preferably inside the ROMS folder)
2. *Run Compiler.py* and pick your program from the file dialog.
3. *Do not move the ROM.txt*. It will generate next to the source code. The CPU expects the file to be in its dedicated place.
4. *Run CPU.py*
5. *Read the results* at the end of the program. It will be excellent for debugging

# ISA

You can see what the opcodes do by reading the comments from line 91-311 in CPU.py

# Tips

When writing programs, you might come across the opcodes "Ram2Rom"(see lines 177-178) and Jump opcodes(see lines 233-279). To know where to jump, you can know the ROM address of a specific operand or line.

For example in:
            
    3. add 0 1
           ^
you can subtract the line index by 1 which is 3 - 1, and multiply it by 3. In our case its (3 - 1) * 3 = 6. If we want to know a specific operand's address in the ROM, you can count where it is on the line like this:

        0  1 2
    3. add 0 1
           ^

get our result from (3 - 1) * 3 = 6 and add the number index of the operand, which in our case is 1. so the full formula is ((3 - 1) * 3) + 1 = 7

# Made something?

If you write a program for this CPU, open an issue or send a PR. I'd love to see what you make
