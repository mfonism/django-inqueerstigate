from contextlib import closing

import numpy as np
import PIL.Image


def load_image_file(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    Improves on `face_recognition.load_image_file()` by releasing opened
    PIL images when the function returns

    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    with closing(PIL.Image.open(file)) as im:
        if mode:
            im = im.convert(mode)
        return np.array(im)
