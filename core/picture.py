from PIL import Image
import numpy as np


def image_to_array(filename):
    # https: // stackoverflow.com / questions / 49271913 / convert - numpy - array - to - rgb - image
    picture = Image.open(filename)
    nparray = np.asarray(picture, dtype=np.float)
    return nparray


def linear_scaling(array):
    return array / 255


def initial_position_velocity_picture(filename):
    narray = image_to_array(filename)
    redarray = narray[:, :, 0]/255
    position = 1 * redarray
    bluearray = linear_scaling(narray[:, :, 2])
    velocity = 1 * bluearray
    return position, velocity


def initial_params_picture(filename):
    narray = image_to_array(filename)
    redarray = linear_scaling(narray[:, :, 0])
    E = 100 * redarray
    greenarray = linear_scaling(narray[:, :, 1])
    over_density = 10 * greenarray
    bluearray = linear_scaling(narray[:, :, 2])
    B = bluearray
    return E, over_density, B


def initial_conditions_pictures(pvimage, paramimage):
    position, velocity = initial_position_velocity_picture(pvimage)
    E, over_density, B = initial_params_picture(paramimage)
    image_height, image_width = position.shape
    initial_conditions = np.zeros((5, image_height, image_width))
    initial_conditions[0, :, :] = position
    initial_conditions[1, :, :] = velocity
    initial_conditions[2, :, :] = E
    initial_conditions[3, :, :] = over_density
    initial_conditions[4, :, :] = B
    print(initial_conditions)
    return initial_conditions


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