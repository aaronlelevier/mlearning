"""
COCO dataset specific logic here
"""
import json
import os
import numpy as np
from mlearning import util


class Annotation:
    """
    For generating COCO dataset formatted annotations from
    Labelme annotations' format
    """

    def __init__(self, path):
        self.path = path

    def all(self):
        """
        Return Lableme Annotations in the COCO Dataset 2014 format
        """
        pass

    def generate(self, output_path):
        """
        Writes the COCO Dataset generated annotations JSON to a file

        Args:
            output_path (str): absolute path to write output
        """
        pass

    def list_annotations(self):
        return [os.path.join(self.path, f)
            for f in os.listdir(self.path)
            if os.path.isfile(os.path.join(self.path, f))]

    def get_categories(self):
        """
        Returns the 'categories' key of the COCO dataset annotation
        """
        cats = {}
        i = 1
        for file in self.list_annotations():
            data = util.load_json(file)

            for shape in data['shapes']:
                label = shape['label']
                if label not in cats:
                    cats[label] = {
                        'id': i,
                        'supercategory': label,
                        'name': label
                    }
                    i += 1
        return list(cats.values())

    def get_images(self):
        """
        Returns the 'images' key of the COCO dataset annotation
        """
        return [self.get_image_ann(f) for f in self.list_annotations()]

    def get_image_ann(self, path):
        """
        Takes the path of a "labelme" style annotation and returns
        a COCO dataset syle image annotation
        """
        ann = util.load_json(path)
        filename, _ = os.path.splitext(os.path.basename(ann['imagePath']))
        return {
            'id': int(filename),
            'height': ann['imageHeight'],
            'width': ann['imageWidth'],
            'file_name': os.path.basename(ann['imagePath'])
        }

    def get_annotation_bbox(self, labelme_bb):
        np_bbs = np.array(labelme_bb)
        bbs = np.reshape(np_bbs, (-1, 4))
        return np.array(
            [bbs[:,0], bbs[:,1], bbs[:,2]-bbs[:,0], bbs[:,3]-bbs[:,1]]
        ).T.squeeze().tolist()

    def label_to_category_id_map(self):
        return {x['name']: x['id'] for x in self.get_categories()}

    def get_segmentation(self, labelme_seg):
        return np.expand_dims(
            np.array(labelme_seg).reshape(-1), axis=0).tolist()

    def get_annotations(self):
        """
        Returns the 'annotations' key of the COCO dataset annotation
        """
        pass
