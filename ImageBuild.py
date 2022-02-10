import time
import imageio

def build(blackMask, linedMask, height, width, imageOutput, imageName):
    """
    Visual tool to demonstrate and export search results for suspicious blocks in the image.
    'blackMask': image clone showing the suspicious blocks with a black and white pattern
    'linedMask': image clone showing the suspicious blocks with a green edge pattern
    'height': height of the image
    'width': width of the image
    'imageOutput': image output path
    'imageName': image name
    """
    # Line edge from the original image (visual purpose)
    for x in range(2, height - 2):
        for y in range(2, width - 2):
             if blackMask[x, y] == 255 and \
                (blackMask[x + 1, y] == 0 or
                blackMask[x - 1, y] == 0 or
                blackMask[x, y + 1] == 0 or
                blackMask[x, y - 1] == 0 or
                blackMask[x - 1, y + 1] == 0 or
                blackMask[x + 1, y + 1] == 0 or
                blackMask[x - 1, y - 1] == 0 or
                blackMask[x + 1, y - 1] == 0):
                    # Edge line - left-upper, right-upper, left-down, right-down
                    if blackMask[x - 1, y] == 0 and \
                        blackMask[x, y - 1] == 0 and \
                        blackMask[x - 1, y - 1] == 0:
                            linedMask[x - 2:x, y, 1] = 255
                            linedMask[x, y - 2:y, 1] = 255
                            linedMask[x - 2:x, y - 2:y, 1] = 255
                    elif blackMask[x + 1, y] == 0 and \
                        blackMask[x, y - 1] == 0 and \
                        blackMask[x + 1, y - 1] == 0:
                            linedMask[x + 1:x + 3, y, 1] = 255
                            linedMask[x, y - 2:y, 1] = 255
                            linedMask[x + 1:x + 3, y - 2:y, 1] = 255
                    elif blackMask[x - 1, y] == 0 and \
                        blackMask[x, y + 1] == 0 and \
                        blackMask[x - 1, y + 1] == 0:
                            linedMask[x - 2:x, y, 1] = 255
                            linedMask[x, y + 1:y + 3, 1] = 255
                            linedMask[x - 2:x, y + 1:y + 3, 1] = 255
                    elif blackMask[x + 1, y] == 0 and \
                        blackMask[x, y + 1] == 0 and \
                        blackMask[x + 1, y + 1] == 0:
                            linedMask[x + 1:x + 3, y, 1] = 255
                            linedMask[x, y + 1:y + 3, 1] = 255
                            linedMask[x + 1:x + 3, y + 1:y + 3, 1] = 255

                    # Straigh line - upper, down, left, right line
                    elif blackMask[x, y + 1] == 0:
                        linedMask[x, y + 1:y + 3, 1] = 255
                    elif blackMask[x, y - 1] == 0:
                        linedMask[x, y - 2:y, 1] = 255
                    elif blackMask[x - 1, y] == 0:
                        linedMask[x - 2:x, y, 1] = 255
                    elif blackMask[x + 1, y] == 0:
                        linedMask[x + 1:x + 3, y, 1] = 255

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    imageio.imwrite(imageOutput / (timestamp + "_" + imageName), blackMask)
    imageio.imwrite(imageOutput / (timestamp + "_lined_" + imageName), linedMask)