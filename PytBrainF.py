#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Volfondr
#
# Created:     28.06.2013
# Copyright:   (c) Volfondr 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zlib

class PNGWrongHeaderError(Exception):
    pass

class PNGNotImplementedError(Exception):
    pass


class PngReader():
    def __init__(self, filepath):
        self.rgb = []
        self.chunks = []

        with open(filepath, mode='rb') as f:
            self.binary = f.read()

        self._getPixels()

    def _checkHeader(self):
        signature = self.binary[:8]
        if (signature != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()
        self.binary = self.binary[8:]

    def _bytes_to_num(self, bytes):
        n = 0
        for b in bytes:
            n = n*256 + b
        return n

    def _getChunks(self):
        while self.binary:
            chunk = []
            length = self._bytes_to_num(self.binary[:4])
            self.binary = self.binary[4:]

            type = self.binary[:4]
            self.binary = self.binary[4:]

            data = self.binary[:length]
            self.binary = self.binary[length:]
            self.binary = self.binary[4:]

            chunk.append(type)
            chunk.append(data)

            self.chunks.append(chunk)

    def _getIHDR(self):
        if(self.chunks[0][0] != b'IHDR'):
            raise PNGNotImplementedError()
        data = self.chunks[0][1]

        self.width = self._bytes_to_num(data[:4])
        self.height = self._bytes_to_num(data[4:8])

        if self._bytes_to_num(data[8:9]) != 8 or self._bytes_to_num(data[9:10]) != 2 or self._bytes_to_num(data[10:11]) != 0 or self._bytes_to_num(data[11:12]) != 0 or self._bytes_to_num(data[12:13]) != 0:
            raise PNGNotImplementedError()


    def _getData(self):
        data = b''
        for i in range(1, len(self.chunks)):
            if(self.chunks[i][0] == b'IDAT'):
                data += self.chunks[i][1]

        return zlib.decompress(data)

    def _pixPlus(self, pix1, pix2):
        return ((pix1[0]+pix2[0])%256,(pix1[1]+pix2[1])%256,(pix1[2]+pix2[2])%256)

    def _peath_predictor(self, pix1, pix2, pix3):
        pix = tuple()
        for i in range(0,3):
            p = (pix1[i] + pix2[i] - pix3[i])
            pa = abs(p-pix1[i])
            pb = abs(p-pix2[i])
            pc = abs(p-pix3[i])

            if(pa <= pb and pa <= pc):
                pix += (pix1[i],)
            elif(pb <= pc):
                pix += (pix2[i],)
            else:
                pix += (pix3[i],)
        return pix

    def _getPixels(self):
        self._checkHeader()
        self._getChunks()

        self._getIHDR()
        data = self._getData()

        pos = 0
        for row in range(0, self.height):
            filter = data[pos]
            pos += 1
            line = []
            left_pix = (0,0,0)
            upleft_pix = (0,0,0)
            up_pix = (0,0,0)
            for col in range(0, self.width):
                pix = (data[pos], data[pos+1], data[pos+2])
                pos += 3
                if(filter == 0):
                    line.append(pix)
                    left_pix = pix
                elif (filter == 1):
                    left_pix = self._pixPlus(left_pix, pix)
                    line += [left_pix]
                elif (filter == 2):
                    left_pix = self._pixPlus(pix, self.rgb[len(self.rgb)-1][col])
                    line += [left_pix]
                elif (filter == 4):
                    up_pix = self.rgb[len(self.rgb)-1][col]
                    current = self._pixPlus(pix,self._peath_predictor(left_pix, up_pix, upleft_pix))
                    line += [current]
                    left_pix = current
                    upleft_pix = up_pix
            self.rgb += [line]


class BrainFuck:

    def __init__(self, data, memory = b'\x00', memory_pointer = 0):
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

class BrainLoller:

    def __init__ (self, filepath):
        self.data = self._getCode(filepath)
        print(self.data)

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



def main():
    #x = PngReader("test_data/sachovnice.png")
    #print(x.rgb)
    y = BrainFuck("test_data/numwarp_input.b")
    z = BrainLoller("test_data/HelloWorld.png")


if __name__ == '__main__':
    main()