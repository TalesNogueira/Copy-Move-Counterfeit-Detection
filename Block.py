import numpy as np
from sklearn.decomposition import PCA

class Block(object):
    def __init__(self, imageBlock, x, y, blockSize):
        """
        Starts an block object used to store cropped parts of the image.
            'imageBlock': cropped part of the image
            'x': x coordenate of the block
            'y': y coordenate of the block
            'blockSize': size of the block
        """
        self.image = imageBlock
        self.imagePixels = self.image.load()

        self.coordinate = (x, y)
        self.blockSize = blockSize

    def appendBlock(self):
        """
        Compute the PCA and append it - and the coordinates - in the data list of the block; returns data list of the block.
        """
        blockData = []

        blockData.append(self.coordinate)
        blockData.append(self.principalComponentAnalysis(precision = 5)) # Is relative to the numbers after the comma of the component in question

        return blockData

    def principalComponentAnalysis(self, precision):
        """
        Compute the average PCA value of the block based in it components; returns the PCA.
        'Precision': number of numbers after the comma in the elements made by the PCA transform
        """
        pca = PCA(n_components=1)

        imageArray = np.array(self.image)
        pca.fit_transform(imageArray)

        principalComponents = pca.components_

        result = [round(element, precision)
                 for element in list(principalComponents.flatten())] # Approximates the block to a single value based on its pixels via linearized PCA

        return result
