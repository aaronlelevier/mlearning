import json

import cv2


def load_json(path):
    "Loads JSON as a Python object from a given file path"
    with open(path) as f:
        data = json.loads(f.read())
    return data


def open_image(image_path):
    """
    Returns an image as a RGB np.ndarray

    Args:
        image_path (str): image path
    Returns:
        np.ndarray
    """
    bgr_img = cv2.imread(image_path)
    # get b,g,r
    b,g,r = cv2.split(bgr_img)
    # switch it to rgb
    return cv2.merge([r,g,b])
