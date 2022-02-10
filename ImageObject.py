import math
import time
import tqdm

import numpy as np
from PIL import Image

import Block
import Container
import ImageBuild

class ImageObject(object):
    def __init__(self, inPath, fileName, outPath, blockSize):
        """
        Starts an image object used to look for and possibly find fakes of the type Copy-Move.
        'inPath': image input path
        'fileName': image name
        'outPath': image output path
        'blockSize': size of the cropped blocks
        """
        self.imageOutput = outPath
        self.imageName = fileName
        self.imageData = Image.open(inPath)
        self.imageWidth, self.imageHeight = self.imageData.size

        self.imageGrayscale = self.imageData.convert('L')
        self.imageGrayscalePixels = self.imageGrayscale.load()

        # Parameters
        self.blockSize = blockSize
        self.offsetBlocks = 188                 # Refers to minimum treshold of blocks per suspicious offsets
        self.minMagnitude = 50                  # Refers to maximum treshold of the offset's magnitude

        # Container initialization to later contains several data (blocks)
        self.blockContainer = Container.Container()
        self.offsetDictionary = {}

    def run(self):
        """
        Run all the principal functions relatives to the image Copy-Move detection.
        """
        start_timestamp = time.time()
        self.crop()
        timestamp_after_computing = time.time()
        self.analyze()
        timestamp_after_analyze = time.time()
        self.reconstruct()
        timestamp_after_image_creation = time.time()

        print("     > Computing time:", timestamp_after_computing - start_timestamp, " seconds(s).")
        print("     > Analyzing time:", timestamp_after_analyze - timestamp_after_computing, " second(s).")
        print("     > Image creation:", timestamp_after_image_creation - timestamp_after_analyze, " second(s).")

        total_running_time_in_second = timestamp_after_image_creation - start_timestamp
        total_minute, total_second = divmod(total_running_time_in_second, 60)
        total_hour, total_minute = divmod(total_minute, 60)
        print("> Total time: %d:%02d:%02d second(s)." % (total_hour, total_minute, total_second), '\n')

    def crop(self):
        """
        Crop the original image in blocks, keeping appending them in a container of data.
        """
        imageWidthOverlap = self.imageWidth - self.blockSize
        imageHeightOverlap = self.imageHeight - self.blockSize

        print("> Starting computing process.")
        for i in tqdm.tqdm(range(imageWidthOverlap + 1)):
            for j in range(imageHeightOverlap + 1):
                imageBlockGrayscale = self.imageGrayscale.crop((i, j, i + self.blockSize, j + self.blockSize))
                imageBlock = Block.Block(imageBlockGrayscale, i, j, self.blockSize)
                self.blockContainer.appendContainer(imageBlock.appendBlock())

    def analyze(self):
        """
        Sort the blocks container by the PCA and compare them, resulting in possible agroupments of fake blocks in the image.
        """
        self.blockContainer.sortByPCA()         # Compare blocks with closest and similar values
        blockContainerLength = self.blockContainer.getLenght()

        print("> Starting analyzing process.")
        for i in tqdm.tqdm(range(blockContainerLength - 1)):
            j = i + 1
            result = self.compareBlocks(i, j)   # Blocks that are too similar that are at a distance above the defined are suspicious and are considered possible Copy-Move
                                                # Noting the coordinates of both blocks and the magnetude between them 
            if result[0]:
                self.addDictionary(self.blockContainer.container[i][0], self.blockContainer.container[j][0], result[1])

    def compareBlocks(self, firstBlock, secondBlock):
        """
        Calculates the distance between two blocks to determine the displacement and magnitude (displacement modulus) of both.
        'firstBlock': first block to be compared
        'secondBlock': second block to be compared
        """
        firstCoordinates = self.blockContainer.container[firstBlock][0]
        secondCoordinates = self.blockContainer.container[secondBlock][0]

        offset = (
            firstCoordinates[0] - secondCoordinates[0],
            firstCoordinates[1] - secondCoordinates[1])

        magnitude = np.sqrt(math.pow(offset[0], 2) + math.pow(offset[1], 2))    # Module of the distance of 'x' and 'y' of both blocks 
        if magnitude >= self.minMagnitude:                                      # Blocks that are too close are naturally similar 
            return 1, offset
        
        return 0,

    def addDictionary(self, firstCoordinate, secondCoordinate, pairOffset):
        """
        Adds coordinates of both similar blocks in the offset/block dictionary using the offset between them as index. 
        'firstCoordinate': coordinates of the first block
        'secondCoordinate': coordinates of the second block
        'pairOffset': offset of two blocks with similar PCA
        """
        if pairOffset in self.offsetDictionary:
            self.offsetDictionary[pairOffset].append(firstCoordinate)
            self.offsetDictionary[pairOffset].append(secondCoordinate)
        else:
            self.offsetDictionary[pairOffset] = [firstCoordinate, secondCoordinate]

    def reconstruct(self):
        """
        Reconstruct the image using the suspicious blocks to identify possible fakes by Copy-Move.
        """
        blackMask = np.zeros((self.imageHeight, self.imageWidth))
        linedMask = np.array(self.imageData.convert('RGB'))

        sorted_offset = sorted(self.offsetDictionary, key=lambda key: len(self.offsetDictionary[key]), reverse=True)

        pairFound = False

        for key in sorted_offset:
            if self.offsetDictionary[key].__len__() < self.offsetBlocks * 2: # Minimum number of similar blocks in an offset 
                break

            if pairFound == False:
                print('> Found pair(s) of possible fraud attack:')
                pairFound = True

            print("     ", key, self.offsetDictionary[key].__len__())

            for i in range(self.offsetDictionary[key].__len__()):           # At the current offset, we cycle through all annotated blocks 
                if (self.offsetDictionary[key][i][0] + self.blockSize > self.imageWidth) or (self.offsetDictionary[key][i][1] + self.blockSize > self.imageHeight):
                    break
                
                for j in range(self.offsetDictionary[key][i][1],
                        self.offsetDictionary[key][i][1] + self.blockSize):                    
                    for k in range(self.offsetDictionary[key][i][0],
                        self.offsetDictionary[key][i][0] + self.blockSize):

                        blackMask[j][k] = 255
        
        if pairFound == False:
            print('> No pair of possible fraud attack found.')

        print("> Blocksize used was "+ str(self.blockSize) +".")

        ImageBuild.build(blackMask, linedMask, self.imageHeight, self.imageWidth, self.imageOutput, self.imageName)

        

        