from PIL import Image, ImageOps
from scipy.ndimage.measurements import center_of_mass
import numpy as np


def preprocess_image(input_file):
    """Prepare input file to recognition process

    Function converts image to proper format size and centers image around center of mass.
    Resulting image is then converted to numpy array and reshaped to match model input format.

    :param input_file: file object to read image from
    :return:
    """
    # open input file
    img = Image.open(input_file)

    # convert image to single channel and invert
    inverted_img = ImageOps.invert(img.convert('L'))

    # crop image to match the bounding box
    cropped_img = inverted_img.crop(inverted_img.getbbox())

    # scale image to fit in 20x20px box
    cropped_img.thumbnail((20, 20))

    # convert image to numpy array
    np_img = np.array(cropped_img)
    mass_center = center_of_mass(np_img)

    # create final 28x28 image and paste centered digit
    final_img = Image.new(mode='L', size=(28, 28))
    point = (14 - int(round(mass_center[1])), 14 - int((round(mass_center[0]))))
    final_img.paste(cropped_img, point)

    # convert image to numpy array and reshape it
    result = np.array(final_img).reshape((784, ))
    return result


def recognize(input_file):
    """Perform input image preprocessing and recognition

    :param input_file: file-like object containing input image
    :return: recognition results
    """
    img = preprocess_image(input_file)
    return {'status': 'ok'}
