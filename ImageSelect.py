import os
from pathlib import Path

import ImageObject

def select(cwdPath, inPath, blockSize):
    inPath = Path(inPath)
    outPath = Path(cwdPath+"\output")

    if not inPath.exists():
        print("     > Erro: Diretorio de entrada nao existe.")
        exit(1)
    if not outPath.exists():
        os.makedirs(outPath)
        print("     > Aviso: Diretorio de saida nao existe.")
        print("         > Diretorio criado automaticamente.")

    image = ImageObject.ImageObject(inPath, inPath.name, outPath, blockSize)
    image.run()