import matplotlib.pyplot as plt
import numpy as np
 
filepath = 'Day08/Day08_Input.txt'

class ImageData():
    def __init__(self, aData, aWidth, aHeight):
        self.decoded = None
        self.data = aData
        self.width = aWidth
        self.height = aHeight
        self.layersize = aWidth * aHeight
        self.layercount = len(aData) / self.layersize

    def getlayer(self, idx):
        return self.data[idx * self.layersize:(idx + 1) * self.layersize]

    def getrow(self, layer, idx):
        startfrom = (layer * self.layersize) + (idx * self.width)
        return self.data[startfrom:startfrom + self.width]

    def getpixel(self, x, y):
        ls = self.layersize
        w = self.width
        h = self.height
        for l in range(0, self.layercount):
            idx = (l * ls) + (x * w) + y
            pixel = self.data[idx:idx + 1]
            if (pixel != '2'):
                return pixel
        else:
            return '2'

    def getdecoded(self):
        if (self.decoded != None):
            return self.decoded
        decoded = ""
        for x in range(0, self.height):
            for y in range(0, self.width):
                decoded = decoded + self.getpixel(x, y)
        else:
            self.decoded = np.fromiter(decoded, dtype=int).reshape(self.height, self.width)
            return self.decoded

def main(width, height):
    with open(filepath) as fp:
        image = ImageData(fp.readline().strip(), width, height)

        plt.imshow(image.getdecoded(), cmap="gray")
        plt.title('Day08_Part2')
        plt.show(block=False)
        plt.pause(0.1) #give time to finish drawing

if __name__ == '__main__':
    print ("Output: " + str(main(25, 6)))