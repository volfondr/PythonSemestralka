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


class PngReader():
    def __init__(self, filepath):
        self.rgb = []
        self.chunks = []

        with open(filepath, mode='rb') as f:
            self.binary = f.read()

        self._getPixels()

    def _checkHeader():
        signature = self.binary[:8]
        if (signature != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()
        self.binary = self.binary[8:]

    def _getChunks():
        while self.binary:
            chunk = []
            length = struck.unpack('>I', bytes[:4])[0]
            self.binary[4:]

            type = self.binary[:4]
            self.binary[4:]

            data = self.binary[:length]
            self.binary[length:]
            self.binary[4:]

            chunk.append(type)
            chunk.append(data)

            self.chunks.append(chunk)

    def _getIHDR():
        if(self.chunks[0][0] != b'IHDR'):
            raise PNGNotImplementedError()
        data = self.chunks[0][1]

        self.width = _bytes_to_num(data[:4])
        self.height = _bytes_to_num(data[4:8])

        if _bytes_to_num(data[8:9]) != 8 or _bytes_to_num(data[9:10]) != 2 or _bytes_to_num(data[10:11]) != 0 or _bytes_to_num(data[11:12]) != 0 or _bytes_to_num(data[12:13]) != 0:
            raise PNGNotImplementedError()


    def _getData():
        for i in range(1, len(chunks)):
            if(chunks[i][0] == b'IDAT'):
                data += chunks[i][1]

        return zlib.decompress(data)

    def _pixPlus(pix1, pix2):
        return ((pix1[0]+pix2[0])%256,(pix1[1]+pix2[1])%256,(pix1[2]+pix2[2])%256)

    def _getPixels():
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
            for col in range(0, self.width):
                pix = (data[pos], data[pos+1], data[pos+2])
                pos += 3
                if(filter == 0):
                    line.append(pix)
                    left_pix = pix
                elif (filter == 1):


def main():
    pass

if __name__ == '__main__':
    main()