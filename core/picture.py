from PIL import Image
import numpy as np

def image_to_array(filename):
    # https: // stackoverflow.com / questions / 49271913 / convert - numpy - array - to - rgb - image
    picture = Image.open("%s" %filename)
    nparray = np.asarray(picture, dtype=np.float)
    return nparray

def array_to_param(array):
    E = array[:,:,0]
    overdensity = array[:,:,1]
    B = array[:,:,2]
    return E, overdensity, B

def scale_array(array):
    return np.arctan(array)/(np.pi*0.5)


def array_to_image(array):
    # Need to pass scaled arrays.
    height, width = array.shape
    one = np.ones((height, width))
    absolutes = np.abs(array)

    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :, 1] = (one - absolutes) * 255
    image[:, :, 2] = (2*one - array - absolutes)/2 * 255
    image[:, :, 0] = (2*one + array - absolutes)/2 * 255

    image = Image.fromarray(image, "RGB")
    return image