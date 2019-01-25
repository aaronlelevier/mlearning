import os
import json
import numpy as np
from matplotlib import patches, patheffects
from matplotlib import pyplot as plt


def load_json(path):
    "Loads JSON as a Python object from a given file path"
    with open(path) as f:
        data = json.loads(f.read())
    return data


def get_image_id_to_image_ann(ann_path):
    ann = load_json(ann_path)
    return {x['id']: x for x in ann['images']}


def get_category_id_to_name():
    """
    Returns a dict where they key is an int and the value is the category
    """
    return {i:c for i,c in enumerate(CATEGORIES)}


def show_img(im, figsize=None, ax=None):
    if not ax:
        _, ax = plt.subplots(figsize=figsize)
    ax.imshow(im)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return ax


def open_image(image_path):
    """
    Returns an image as a rgb np.ndarray
    """
    bgr_img = cv2.imread(image_path)
    # get b,g,r
    b,g,r = cv2.split(bgr_img)
    # switch it to rgb
    return cv2.merge([r,g,b])/255.


def get_imageid_to_anns(ann_path):
    """
    Returns a dict where the key is an imageid and the value
    is a list of annotations for that image
    """
    ann = load_json(ann_path)

    imageid_to_anns = {}
    for img in ann['images']:
        imageid_to_anns[img['id']] = []

    for a in ann['annotations']:
        imageid_to_anns[a['image_id']].append(a)

    return imageid_to_anns


def get_albu_ann():
    bboxes = [x['bbox'] for x in people_anns]
    category_ids = [x['category_id'] for x in people_anns]


CATEGORIES = [
    "__background",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


def get_image_anns(dirpath):
    ret = []
    for f in list_files(dirpath):
        filepath = os.path.join(dirpath, f)
        ret.append(get_image_ann(filepath))
    return ret


def list_files(path):
     return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_image_ann(path):
    """
    Takes the path of a "labelme" style annotation and returns
    a COCO dataset syle image annotation
    """
    ann = load_json(path)
    filename, _ = os.path.splitext(os.path.basename(ann['imagePath']))
    return {
        'id': int(filename),
        'height': ann['imageHeight'],
        'width': ann['imageWidth'],
        'file_name': os.path.basename(ann['imagePath'])
    }
