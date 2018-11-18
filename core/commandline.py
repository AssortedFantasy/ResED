from core import picture
from core import sim
import numpy as np
import sys

if __name__ == "__main__":
    print("python3 commandline.py <pvimage> <paraimage> <image_height> <image_width>")
    picture.initial_conditions_pictures(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])