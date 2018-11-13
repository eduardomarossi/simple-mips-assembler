#!/usr/bin/python3
# author: Eduardo Marossi <eduardom44@gmail.com>

import logging
import argparse
import sys

class Line_Assemble:
    def __init__(self):
        self.r_instructions = ['add', 'sub', 'and', 'or', 'slt']
        self.i_instructions = ['lw', 'sw', 'beq']
        self.j_instructions = ['j']
    
    def set_line(self, line):
        self.line = line.strip().replace('  ', ' ')
        if self.line.find(';') != -1:
            self.line = self.line[0:self.line.find(';')]

        logging.debug('set line: {}'.format(self.line))

    def get_parts(self):
        instruct = self.line[:self.line.find(' ')].replace(' ', '')
        args = self.line[self.line.find(' '):].replace(' ', '')
        logging.debug('parts: {} {}'.format(instruct, args))
        return (instruct, args.split(','))

    def get_instruction_type(self):
        instruct = self.get_parts()[0]
        if instruct in self.r_instructions:
            tp = 'r'
        elif instruct in self.i_instructions: 
            tp = 'i'
        elif instruct in self.j_instructions:
            tp = 'j'
        logging.debug('type: {}'.format(tp))
        return tp

    def get_instruction(self):
        instruct, args = self.get_parts()
        output = ""
        if self.get_instruction_type() == 'r':
            output = "000000" + self.get_register(args[1]) + self.get_register(args[2]) + self.get_register(args[0]) + "00000" + self.get_r_funct(instruct)
        elif self.get_instruction_type() == 'i' and len(args) == 2:
            output = self.get_i_instruction(instruct) + self.get_register(args[1]) + self.get_register(args[0]) + self.get_immediate(args[1])
        elif self.get_instruction_type() == 'i' and len(args) == 3:
            output = self.get_i_instruction(instruct) + self.get_register(args[1]) + self.get_register(args[0]) + self.get_immediate(args[2])
        elif self.get_instruction_type() == 'j':
            output = self.get_j_instruction(instruct) + self.get_j_immediate(args[0])
        logging.debug('instruction: {}'.format(output))
        return output
        
    def get_r_funct(self, instruct):
        table = {'add': '20', 'sub': '22', 'and': '24', 'or':'25', 'slt':'2a', 'nop': '0'}
        r = "{0:b}".format(int(table[instruct], 16)).zfill(6)
        logging.debug('r funct: {}'.format(r))
        return r

    def get_i_instruction(self, instruct):
        table = {'lw': '23', 'sw':'2b', 'beq':'4'}
        r = "{0:b}".format(int(table[instruct], 16)).zfill(6)
        logging.debug('i instruct: {}'.format(r))
        return r
 
    def get_j_instruction(self, instruct):
        table = {'j': '2'}
        r = "{0:b}".format(int(table[instruct], 16)).zfill(6)
        logging.debug('j instruct: {}'.format(r))
        return r

    def get_register(self, register):
        register = register.strip().replace(' ', '')
        if '(' in register:
            register = register[register.find('('):register.find(')')]

        if '$' in register:
            register = register[register.find('$')+1:]

        table = {'zero': '0', 'at' : '1', 'v0' : '2', 'v1': '3', 'a0' : '4', 'a1': '5', 'a2': '6', 'a3': '7', 't0': '8',
                 't1': '9', 't2': '10', 't3' : '11', 't4': '12', 't5': '13', 't6': '14', 't7': '15', 's0': '16', 
                 's1': '17', 's2': '18', 's3': '19', 's4': '20', 's5': '21', 's6': '22', 's7': '23', 't8': '24',
                 't9': '25', 'k0': '26', 'k1': '27', 'gp': '28', 'sp' : '29', 'fp': '30', 'ra': '31'}

        r = "{0:b}".format(int(table[register])).zfill(5) 
        logging.debug('register: {}'.format(r))
        return r
        

    def get_immediate(self, immediate):
        if '(' in immediate:
            immediate = immediate[0:immediate.find('(')]

        r = "{0:b}".format(int(immediate)).zfill(16)
        logging.debug('immediate: {}'.format(r))
        return r

    def get_j_immediate(self, immediate):
        r =  "{0:b}".format(int(immediate)).zfill(26) 
        logging.debug('j immediate: {}'.format(r))
        return r


class MIPS_Assemble:
    def __init__(self):
        self.read_stream = None
        self.write_stream = None

    def set_load_file(self, file_stream):
        self.read_stream = file_stream

    def assemble(self):
        line_asm = Line_Assemble()
        for i, l in enumerate(self.read_stream):
            line_asm.set_line(l)
            self.write_stream.write(line_asm.get_instruction() + "\n")

    def set_save_file(self, file_stream):
        self.write_stream = file_stream

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('in_file', type=str)
    argparse.add_argument('-d', '--debug', default=False, action='store_true')
    args = argparse.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    mips = MIPS_Assemble()
    mips.set_load_file(open(args.in_file, 'r'))
    mips.set_save_file(sys.stdout)
    mips.assemble()
    