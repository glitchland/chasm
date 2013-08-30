#!/usr/bin/python

import argparse
import os
import array

import chasm


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("The file %s does not exist!"%arg)
    else:
       return open(arg,'rb')  #return an open file handle

def write_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("The file %s does not exist!"%arg)
    else:
       return open(arg,'w+')  #return an open file handle    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip8 Disassembler')
    parser.add_argument('-i', dest="filename", required=True, help='c8',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', dest="output", help='asm file',
                        type=lambda file: is_valid_file(parser, file))
    args = parser.parse_args()

    opcodes = array.array('H')

    try:
        opcodes.fromfile(args.filename, 1024)
    except EOFError:
        pass

    mnemonics = chasm.disassembler.generate(opcodes)
    args.output.write('\n'.join(mnemonics))
    args.output.close()