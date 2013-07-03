#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Interpretr jazyka brainfuck."""

    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""

        # data programu
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer

        try:
            with open(data, mode = 'r') as f:
                self.code = f.read()
        except:
            self.code = data

        self.user_input = self._getInput()
        self.output = ""

        self._evaluate(self.code)


    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory

    def _getInput(self):
        pos = 0
        while pos < len(self.code) and self.code[pos] != '!':
            pos += 1

        if pos+1 < len(self.code):
            ret = self.code[pos+1:]
            self.code = self.code[:pos]
            return ret

    def _getChar(self):
        if(len(self.user_input) != 0):
            ret = self.user_input[0]
            self.user_input = self.user_input[1:]
            return ret
        else:
            return sys.stdin.read(1)


    def _getLoop(self, code):
        end = 1
        while (code[0:end].count('[') != code[0:end].count(']')):
            end += 1

        return code[1:end-1]


    def _evaluate(self, code):
        codeptr = 0
        while codeptr < len(code):
            char = code[codeptr]

            if char == ">":
                self.memory_pointer += 1
                if len(self.memory) == self.memory_pointer:
                    self.memory += bytearray([0])

            if char == "<":
                if self.memory_pointer != 0:
                    self.memory_pointer -= 1

            if char == "+":
                if self.memory[self.memory_pointer] == 255:
                    self.memory[self.memory_pointer] == 0
                else:
                    self.memory[self.memory_pointer] += 1

            if char == "-":
                if self.memory[self.memory_pointer] == 0:
                    self.memory[self.memory_pointer] == 255
                else:
                    self.memory[self.memory_pointer] -= 1

            if char == ".":
                print(chr(self.memory[self.memory_pointer]), end=r'')
                #print(self.memory[self.memory_pointer], end=r'')
                self.output += chr(self.memory[self.memory_pointer])

            if char == ",":
                self.memory[self.memory_pointer] = ord(self._getChar())

            if char == "[":
                loop = self._getLoop(code[codeptr:])
                if self.memory[self.memory_pointer] == 0:
                    codeptr += len(loop) + 1
                else:
                    while self.memory[self.memory_pointer] != 0:
                        self._evaluate(loop)
                    codeptr += len(loop) + 1

            codeptr += 1



class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""

    def __init__ (self, filepath):
        self.data = self._getCode(filepath)

        self.program = BrainFuck(self.data)

    def _getChar(self):
        color = self.rgb[self.pos[0]][self.pos[1]]
        if(color == (255,0,0)):
            return '>'
        if(color == (128,0,0)):
            return '<'
        if(color == (0,255,0)):
            return '+'
        if(color == (0,128,0)):
            return '-'
        if(color == (0,0,255)):
            return '.'
        if(color == (0,0,128)):
            return ','
        if(color == (255,255,0)):
            return '['
        if(color == (128,128,0)):
            return ']'
        if(color == (0,255,255)):
            self._turn(0)
            return ""
        if(color == (0,128,128)):
            self._turn(1)
            return ""
        return ""

    def _turn(self, direction):
        if (direction == 1):
            if((self.dir[1]+1) % 2 == 0):
                self.dir[1] = 0
                if((self.dir[0]+1)%2 == 0):
                    self.dir[0] = 0
                else:
                    self.dir[0] = 1
            else:
                self.dir[1] = 1
        else:
            self._turn(1)
            self._turn(1)
            self._turn(1)

    def _step(self):
        if(self.dir[0] == 1 and self.dir[1] == 1):
            self.pos[1] += 1
        if(self.dir[0] == 0 and self.dir[1] == 1):
            self.pos[1] -= 1
        if(self.dir[0] == 1 and self.dir[1] == 0):
            self.pos[0] += 1
        if(self.dir[0] == 0 and self.dir[1] == 0):
            self.pos[0] -= 1


    def _getCode(self, filepath):
        from image_png import PngReader
        self.rgb = PngReader(filepath).rgb
        print(self.rgb)
        self.pos = [0, 0]
        self.dir = [1, 1] #north
        self.ret = ""
        while True:
            self.ret += self._getChar()
            self._step()
            if(self.pos[0] >= len(self.rgb) or self.pos[1] >= len(self.rgb[0]) or self.pos[0] < 0 or self.pos[1] < 0):
                break
        return self.ret


class BrainCopter(BrainLoller):
    """Třída pro zpracování jazyka braincopter."""

    def _getChar(self):
        color = self.rgb[self.pos[0]][self.pos[1]]
        num = (-2*color[0] + 3*color[1] + color[2])%11
        bf = '><+-.,[]'
        if(num < 8):
            return bf[num]
        if num == 8:
            self_turn(0)
        if num == 9:
            self_turn(1)
        return ""

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog [-h] [--version] [-l] [-c] FILE', version="%prog 1.0")
    parser.add_option('-l', '--brainloller', action='store_true', dest='loller',
                        help='usage of the BrainLoller')
    parser.add_option('-c', '--copter', action='store_true', dest='copter',
                        help='usage of the BrainCopter')
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error('too few arguments')
    if options.copter and options.loller:
        parser.error('options --brainloller and --braincopter are mutually exclusive')

    try:
        with open(args[0]): pass
    except IOError:
        parser.error(args[0]+' is not a file or it cannot be opened')

    if options.loller:
        BrainLoller(args[0])
    elif options.copter:
        BrainCopter(args[0])
    else:
        BrainFuck(args[0])
