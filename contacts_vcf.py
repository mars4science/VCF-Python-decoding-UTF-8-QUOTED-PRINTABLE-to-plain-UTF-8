#!/usr/bin/python3
# assumes vcf in the format of line continuation of QUOTED-PRINTABLE of extra "=" at the end, like:
# FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=00=01=02\=
# n=03=04=
# =05=06=07

import argparse
import quopri

parser = argparse.ArgumentParser(description='Process vcf file, decoding UTF-8 QUOTED-PRINTABLE to plain UTF-8', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--ifn', help='file name/path to process')
parser.add_argument('--ofn', help='file name/path to output result')
args = parser.parse_args()
in_file_name = args.ifn
out_file_name = args.ofn

def decode_quopri(line):
    return quopri.decodestring(line)

def decode_line(line):
    return decode_quopri(line).decode('utf-8')

def write_line(f,line):
    f.write(line.replace('\n','\\n') + '\n') # make \\n from \n to write \n to the vcf's line

with open(in_file_name, 'r') as f:
    in_vcf = f.readlines()

f_out = open(out_file_name, 'w')

line_multiple_lines = ''
for line in in_vcf:
    line = line.strip() # Strips the newline character
    if line_multiple_lines != '':
        if line[-1] == '=':
            line_multiple_lines += line[0:-1]
        else:
            write_line(f_out,decode_line(line_multiple_lines + line))
            line_multiple_lines = ''
    else:
        if line.find('ENCODING=QUOTED-PRINTABLE') != -1:
            line = line.replace(';ENCODING=QUOTED-PRINTABLE','')
            line = line.replace(';CHARSET=UTF-8','')
            if line[-1] == '=':
                line_multiple_lines = line[0:-1]
            else:
                write_line(f_out,decode_line(line))
        else:
            write_line(f_out,line)
    
f_out.close()
