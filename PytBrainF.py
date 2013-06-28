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

        self.getPixels()

    def checkHeader():
        signature = self.binary[:8]
        if (signature != b'\x89PNG\r\n\x1a\n'):
            raise WrongHeaderError()
        self.binary = self.binary[8:]

    def getChunks():
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

    def getIHDR():

    def getPixels():
        self.checkHeader()
        self.getChunks()

        getIHDR()


def main():
    pass

if __name__ == '__main__':
    main()