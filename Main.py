import os
import ImageSelect

datasetPath = os.getcwd() + "\dataset\multi_paste"
dataset = {}

index = 0
for x in os.listdir(datasetPath):
    if not x.endswith("mask.png") and not x.endswith("mask.bmp"):
        index += 1
        dataset[index] = x
        print("     "+ str(index) +". "+ str(x))

print("> Choose one of the images from the dataset below by its numbering, to check for possible existing Copy-Move fakes .")
index = input()
image = dataset[int(index)]
print("> The chosen image was  "+ image +".")

print("> Choose the size of the comparison blocks. (Positive and non-zero).")
block = int(input())

if (block <= 0):
    block = 4

ImageSelect.select(os.getcwd(), (datasetPath + "\\" + image), block)