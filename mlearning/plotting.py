"""
Module for displaying image bounding boxes and masks
"""
import numpy as np
import cv2

import json
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from mlearning import util

HOME_DIR = os.path.expanduser('~')

# must adjust the path of DATA_DIR and direct has to contain COCO dataset images
DATA_DIR = os.path.join(HOME_DIR, 'Desktop/license_plate_detection/images/')

# must adjust path and ANN should point to a COCO dataset annotations.json file
ANN = util.load_json(
    os.path.join(HOME_DIR, 'Desktop/license_plate_detection/output/annotations.json'))


def get_imageid_to_imageann(ann):
    return {x['id']: x for x in ann['images']}


def get_imageid_to_anns(ann):
    """
    Returns a dict where the key is an imageid and the value
    is a list of annotations for that image
    """
    imageid_to_anns = {}
    for img in ann['images']:
        imageid_to_anns[img['id']] = []

    for a in ann['annotations']:
        imageid_to_anns[a['image_id']].append(a)

    return imageid_to_anns


IMAGEID_TO_IMAGEANN = get_imageid_to_imageann(ANN)
CATEGORY_ID_TO_NAME = {x['id']: x['name'] for x in ANN['categories']}
IMAGE_IDS = list(IMAGEID_TO_IMAGEANN.keys())
IMAGEID_TO_ANN = get_imageid_to_anns(ann=ANN)


def plot_bboxes_and_masks(image_id=None):
    image_id = image_id or np.random.choice(IMAGE_IDS)
    image_ann = IMAGEID_TO_IMAGEANN[image_id]
    image_path = os.path.join(DATA_DIR, image_ann['file_name'])
    image = util.open_image(image_path)

    # image + bboxes
    bboxes = [x['bbox'] for x in IMAGEID_TO_ANN[image_id]]
    category_ids = [x['category_id'] for x in IMAGEID_TO_ANN[image_id]]
    annotations = {
        'image': image,
        'bboxes': bboxes,
        'category_id': category_ids
    }
    visualize(annotations, CATEGORY_ID_TO_NAME)

    ax = plt.gca()
    polygons = []
    color = []
    anns = IMAGEID_TO_ANN[image_id]
    for ann in anns:
        c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]
        # polygon
        for seg in ann['segmentation']:
            poly = np.array(seg).reshape((int(len(seg)/2), 2))
            polygons.append(Polygon(poly))
            color.append(c)

    p = PatchCollection(polygons, facecolor=color, linewidths=0, alpha=0.4)
    ax.add_collection(p)
    p = PatchCollection(polygons, facecolor='none', edgecolors=color, linewidths=2)
    ax.add_collection(p)


"""
Credit to: albumentations for these 2 functions

https://github.com/albu/albumentations/blob/master/notebooks/example_bboxes.ipynb
"""
BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

def visualize_bbox(img, bbox, class_id, class_idx_to_name, color=BOX_COLOR, thickness=2):
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    class_name = class_idx_to_name[class_id]
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img, class_name, (x_min, y_min - int(0.3 * text_height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35,TEXT_COLOR, lineType=cv2.LINE_AA)
    return img


def visualize(annotations, category_id_to_name):
    img = annotations['image'].copy()
    for idx, bbox in enumerate(annotations['bboxes']):
        img = visualize_bbox(img, bbox, annotations['category_id'][idx], category_id_to_name)
    plt.figure(figsize=(12, 12))
    plt.imshow(img)
