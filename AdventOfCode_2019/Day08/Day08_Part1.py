filepath = 'Day08/Day08_Input.txt'

class ImageData():
    data = []
    width = 0
    heigth = 0
    layercount = 0
    layersize = 0
    def __init__(self, aData, aWidth, aHeight):
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

def main(width, height):
    with open(filepath) as fp:
        image = ImageData(fp.readline().strip(), width, height)

        fewest = width * height
        fewestlayer = 0
        for i in range(0, image.layercount):
            layer = image.getlayer(i)
            zerocount = layer.count('0')
            if zerocount < fewest:
                fewest = zerocount
                fewestlayer = i
        
        layer = image.getlayer(fewestlayer)
        return layer.count('1') * layer.count('2')

if __name__ == '__main__':
    print ("Output: " + str(main(25, 6)))