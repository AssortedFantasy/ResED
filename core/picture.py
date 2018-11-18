from PIL import Image
import numpy as np

def imagetoarray(filename):
    # https: // stackoverflow.com / questions / 49271913 / convert - numpy - array - to - rgb - image
    picture = Image.open("%s" %filename)
    nparray = np.asarray(picture, dtype=np.float16)
    print(nparray)
    print(nparray.shape)
    return nparray

def arraytowave(array):
    E = array[:,:,0]
    overdensity = array[:,:,1]
    B = array[:,:,2]
    print(overdensity)


newarray = imagetoarray("testred.png")
arraytowave(newarray)