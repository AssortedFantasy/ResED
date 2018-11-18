from PIL import Image
import numpy as np

def imagetoarray(filename):
    # https: // stackoverflow.com / questions / 49271913 / convert - numpy - array - to - rgb - image
    picture = Image.open("%s" %filename)
    nparray = np.asarray(picture, dtype=np.float)
    return nparray

def arraytowave(array):
    E = array[:,:,0]
    overdensity = array[:,:,1]
    B = array[:,:,2]
    return E, overdensity, B

def scalearray(array):
    maximum = np.amax(a)
    minimum = np.amin(a)
    if abs(maximum) >= abs(minimum):
        denom = maximum
    elif abs(maximum) < abs(minimum):
        denom = abs(minimum)
    scaledarray = array / denom
    return scaledarray


def rgbsorting(scaledarray):


def arraytoimage(processedarray):
    image = Image.fromarray(processedarray, "RGB")
    image.show()

a = np.array([[0, -1, 2],
             [3, -9.2222, 2],
             [-6, 7, 8]])

b = scalearray(a)
c = arraytoimage(b)