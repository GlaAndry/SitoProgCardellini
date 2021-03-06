##Questa funzione python permette di eseguire il resize di un immagine (da verificare il formato)
##Verranno successivamente aggiunte anche delle resize predefinite, così da cercare di lasciare invariata l'immagine.

from PIL import Image, ImageEnhance

def resize(wSize, hSize, inPath, outPath):
    ##Function for resizing an image:
        #wSize: int --> Largezza
        #hSize: int --> Altezza
        #inPath: str --> Input Path
        #outPath: str --> Output Path

    try:
        img = Image.open(inPath)
        img = img.resize((wSize, hSize), Image.ANTIALIAS)
        img.save(outPath) 
    except IOError:
        print("Impossibile trovare l'immagine")
        exit(1)


def blackAndWhite(inPath, outPath):
    ##Function returns image in B&W
        #inPath: str --> Input Path
        #outPath: str --> Output Path

    try:
        img = Image.open(inPath)
        img = img.convert('L')
        img.save(outPath) 
    except IOError:
        print("Impossibile trovare l'immagine")
        exit(1)


def changeBrightness(inPath, outPath, factor):
    ##Function change Brightness of image
        #inPath: str --> Input Path
        #outPath: str --> Output Path
        #factor: int --> 0.5 Darker, 1 Normal, 1.5 Bright

    try:
        img = Image.open(inPath)
        enancher = ImageEnhance.Brightness(img)
        img = enancher.enhance(factor)
        img.save(outPath) 
    except IOError:
        print("Impossibile trovare l'immagine")
        exit(1)


def changeSaturation(inPath, outPath, factor):
    ##Function change Saturation of image
        #inPath: str --> Input Path
        #outPath: str --> Output Path
        #factor: int --> 0.5 Darker, 1 Normal, 1.5 Bright

    try:
        img = Image.open(inPath)
        enancher = ImageEnhance.Color(img)
        img = enancher.enhance(factor)
        img.save(outPath) 
    except IOError:
        print("Impossibile trovare l'immagine")
        exit(1)
