import cv2
import numpy as np
from skimage.transform import rotate
from skimage.util import random_noise


def add_noise(image, noise_type='gaussian', amount=0.5, mean=0, variance=0.1):
    """
    * Image : ndarray; Input image on which filter wil be applied
    * noise_type : string; Can have one of the following values (default='gaussian')
      1. 'gaussian' : Adds Gaussian-distributed noise to the image with mean=mean and variance = var
          *default mean = 0 and var = 0.1*
      2. 'poisson'  : Adds Poisson-distributed noise to the image
      3.  'salt' :
      4. 'pepper' :
      5. 's&p' :
      6. 'speckle':
    * mean , var : float ; optional , works only with gaussian
    * amount : float; optional, works only with 'salt','pepper','s&p'
    """
    if noise_type in ['salt', 'pepper', 's&p']:
        image_with_noise = random_noise(image, mode=noise_type, amount=amount)
    elif noise_type in ['poisson', 'speckle']:
        image_with_noise = random_noise(image, mode=noise_type)
    else:
        image_with_noise = random_noise(image, mode=noise_type, mean=mean, var=variance)
    return image_with_noise


def crop(image, size):
    """
     * Image : ndarray; Input image on which Crop wil be applied
     * size : dimension in which image is to be  cropped; Ensure that the crop size should be less than image size
    """
    assert size[0] <= image.shape[0] and size[1] <= image.shape[
        1], "Crop size provided is more than the size of the image"
    image = image.copy()
    width, height = image.shape[:2]
    x, y = np.random.randint(height - size[0]), np.random.randint(width - size[1])
    image = image[y:y + size[0], x:x + size[1], :]
    return image


def translate(image, percent_shift=10, direction='left', roll_image=True):
    """
    # Translate image
    # Provides translation along X axis and Y axis

    * Image : ndarray; Input image on which Crop wil be applied
    * percent_shift : float; shift the image in given direction by this amount(default:10)
    * direction :string; ('right','left','up','down')(default:'left')
    * roll_image : boolean ; image will be rolled back if this is true (default : True)
    """
    assert direction in ['right', 'left', 'down', 'up'], 'Directions should be top|up|left|right'
    image = image.copy()
    if direction == 'right':
        shift = int(image.shape[1] * percent_shift / 100)
        right_slice = image[:, -shift:].copy()
        image[:, shift:] = image[:, :-shift]
        if roll_image:
            image[:, :shift] = np.fliplr(right_slice)
    if direction == 'left':
        shift = int(image.shape[1] * percent_shift / 100)
        left_slice = image[:, :shift].copy()
        image[:, :-shift] = image[:, shift:]
        if roll_image:
            image[:, -shift:] = left_slice
    if direction == 'down':
        shift = int(image.shape[0] * percent_shift / 100)
        down_slice = image[-shift:, :].copy()
        image[shift:, :] = image[:-shift, :]
        if roll_image:
            image[:shift, :] = down_slice
    if direction == 'up':
        shift = int(image.shape[0] * percent_shift / 100)
        upper_slice = image[:shift, :].copy()
        image[:-shift, :] = image[shift:, :]
        if roll_image:
            image[-shift:, :] = upper_slice
    return image


def rotate_image(image, deg=45):
    """
    # Rotate Image

    * Image : ndarray; Input image on which Crop wil be applied
    * deg : float; degrees by which image is rotated in counter clockwise direction
    """
    return rotate(image, angle=deg)


def zoom_layer(image, factor=1):
    h, w = image.shape
    m = cv2.getRotationMatrix2D((w / 2, h / 2), 0, factor)
    return cv2.warpAffine(image, m, image.shape[::-1])


def zoom(image, factor=1):
    """
    # Zoom In or Zoom Out
    Image : ndarray; Input image on which Crop wil be applied
    factor: float; zoom in if factor>1 , zoom out if factor<1
    """
    zoomed_image = image.copy()
    for i in range(image.shape[2]):
        zoomed_image[:, :, i] = zoom_layer(image[:, :, i], factor)
    return zoomed_image
