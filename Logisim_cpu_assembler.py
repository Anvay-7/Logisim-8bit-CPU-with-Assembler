import re
opcodes = {'AND': '0', 'OR': '1', 'ADD': '2', 'SUB': '3', 'LW': '4', 'SW': '5', 'MOV': '6',
           'NOP': '7', 'JEQ': '8', 'JNE': '9', 'JGT': 'a', 'JLT': 'b', 'LI': 'e', 'JMP': 'f'}
lines = []
labels = {}
line_codes = []
file = open("D:\\verilog codes\code_asm.txt", "r+")

line_address = {}
line_size = {}

def find_line_address_and_size(lines):
    address = 0
    size = 0
    for line_no, line in enumerate(lines):
        address = address+size
        line_address[line_no+1] = format(address, '02x')
        if re.match(r'(0x[0-9|a-f]{2}$)|(?!\(?R[0-3]\)?)', line[-1], re.I):
            size = 2
        else:
            size = 1
        line_size[line_no+1] = size


def convert_Reg_to_code(Rd, Rs):
    Rd = format(int(re.search(r'\(?R([0-3])\)?', Rd).group(1)), '02b')
    Rs = format(int(re.search(r'\(?R([0-3])\)?', Rs).group(1)), '02b')
    code = format(int(Rd+Rs, 2), 'x')
    return code


index = 0
while True:
    line = file.readline()
    if not line:
        break
    lines.append(line[0:line.find('#')].strip())
    # print(lines[index])
    lines[index] = re.split(r'\s+,*|,+\s*', lines[index])
    index += 1
file.close()
# print(lines)
find_line_address_and_size(lines)

for line_no, line in enumerate(lines):
    if line[0].find(':') != -1:
        labels[line[0][0:line[0].find(':')]] = line_address[line_no+1]

for line_no, line in enumerate(lines):
    if re.match(r'\w+:', line[0]):
        offset = 1
    else:
        offset = 0

    if line_size[line_no+1] == 2:
        opcodes['LW'], opcodes['SW'] ='c','d'
        if line[0+offset].upper() != 'JMP':
            line_codes.append(opcodes[line[0+offset]] + convert_Reg_to_code(line[1+offset], 'R0'))
            if re.match(r'(0x[0-9|a-f]{2}$)', line[-1], re.I):
                line_codes.append(line[2+offset][2:])
            else:
                line_codes.append(labels[line[2+offset]])
        else:
            line_codes.append(opcodes[line[0+offset]] + convert_Reg_to_code('R3', 'R3'))
            if re.match(r'(0x[0-9|a-f]{2}$)', line[-1], re.I):
                line_codes.append(line[1+offset][2:])
            else:
                line_codes.append(labels[line[1+offset]])
    else:
        opcodes['LW'], opcodes['SW'] ='4','5'
        if line[0+offset].upper() != 'NOP':
            line_codes.append(opcodes[line[0+offset]] + convert_Reg_to_code(line[1+offset], line[2+offset]))
        else:
            line_codes.append(opcodes[line[0+offset]] + convert_Reg_to_code('R3', 'R3'))

final_code_str="v2.0 raw\n"
j=0
for line_no,size in line_size.items():
    for i in range(size):
        if i!=size-1:
            final_code_str+=line_codes[j]+" "
        else:
            final_code_str+=line_codes[j]+"\n"
        j+=1

file= open("D:\Documents\Logisim_project_files\\assembled_code.img","w+")
file.write(final_code_str)
file.close()



# print(line_address)
# print(labels)
# print(lines)
# print(line_codes)
# print(final_code_str)
