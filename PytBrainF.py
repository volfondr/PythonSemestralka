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
            pa = abs(p-a[i])
            pb = abs(p-b[i])
            pc = abs(p-c[i])

            if(pa <= pb and pa <= pc):
                pix += (a[i],)
            elif(pb <= pc):
                pix += (b[i],)
            else:
                pix += (c[i],)
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
            for col in range(0, self.width):
                pix = (data[pos], data[pos+1], data[pos+2])
                pos += 3
                if(filter == 0):
                    line.append(pix)
                    left_pix = pix
                elif (filter == 1):
                    left_pixel = self._pixPlus(pix, self.rgb[len(self.rgb)-1][column])
                    line += [left_pixel]
                elif (filter == 4):
                    up_pixel = self.rgb[len(self.rgb)-1][column]
                    current = self._pixPlus(pixel,self._peath_predictor(left_pixel, up_pixel, upleft_pixel))
                    line += [current]
                    left_pixel = current
                    upleft_pixel = up_pixel
            self.rgb += [line]


def main():
    x = PngReader("test_data/sachovnice.png")
    print(x.rgb)

if __name__ == '__main__':
    main()