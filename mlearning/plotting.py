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


def plot_bboxes_and_masks(ann, image_id=None):
    image_ids = ann.get_image_ids()
    imageid_to_ann = ann.get_imageid_to_ann()
    imageid_to_imageann = ann.get_imageid_to_imageann()
    category_id_to_name = ann.get_category_id_to_name()

    image_id = image_id or np.random.choice(image_ids)
    image_ann = imageid_to_imageann[image_id]
    image_path = os.path.join(ann.image_path, image_ann['file_name'])
    image = util.open_image(image_path)

    # image + bboxes
    bboxes = [x['bbox'] for x in imageid_to_ann[image_id]]
    category_ids = [x['category_id'] for x in imageid_to_ann[image_id]]

    annotations = {
        'image': image,
        'bboxes': bboxes,
        'category_id': category_ids
    }
    visualize(annotations, category_id_to_name)

    ax = plt.gca()
    polygons = []
    color = []
    anns = imageid_to_ann[image_id]
    for ann in anns:
        # polygon
        for seg in ann['segmentation']:
            poly = np.array(seg).reshape((int(len(seg)/2), 2))
            polygons.append(Polygon(poly))
            c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]
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
