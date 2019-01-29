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

    This class caches it's data, so it assumes that all Labelme
    annotations, images, and category annotations are present
    in the `path` when the class is instantiated. If new data
    is added, the class needs to be-reinstantiated
    """

    def __init__(self, path):
        """
        Args:
            path (str):
              directory where data is stored. Under this dir
              3 sub dirs should exist:
                - annotations - where Labelme annotations are stored
                - images - images are stored
                - output - dir to output final COCO dataset converted
                           annotations to
        """
        self.ann_path = os.path.join(path, 'annotations')
        self.image_path = os.path.join(path, 'images')
        self.output_path = os.path.join(path, 'output')

        # caches
        self._images = None
        self._annotations = None
        self._categories = None

    def all(self):
        """
        Return Lableme Annotations in the COCO Dataset 2014 format
        """
        return {
            'info': {},
            'images': self.get_images(),
            'licenses': [],
            'annotations': self.get_annotations(),
            'categories': self.get_categories()
        }

    def generate(self, filename='annotations.json'):
        """
        Writes the COCO Dataset generated annotations JSON to a file

        Args:
            filename (str): output filename
        """
        with open(os.path.join(self.output_path, filename), 'w') as f:
            f.write(json.dumps(self.all()))

    def list_annotations(self):
        """
        Returns a list of all labelme annotation files by their abspath's
        """
        return [os.path.join(self.ann_path, f)
                for f in os.listdir(self.ann_path)
                if os.path.isfile(os.path.join(self.ann_path, f))]

    def get_categories(self):
        """
        Returns the 'categories' key of the COCO dataset annotation
        """
        if not self._categories:
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
            self._categories = list(cats.values())
        return self._categories

    def get_images(self):
        """
        Returns the 'images' key of the COCO dataset annotation
        """
        if not self._images:
            self._images = [self.get_image_ann(f) for f in self.list_annotations()]
        return self._images

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

    def get_label_to_category_id_map(self):
        return {x['name']: x['id'] for x in self.get_categories()}

    def get_segmentation(self, labelme_seg):
        return np.expand_dims(
            np.array(labelme_seg).reshape(-1), axis=0).tolist()

    def get_annotations(self):
        """
        Returns the 'annotations' key of the COCO dataset annotation
        """
        if not self._annotations:
            ann_id = 1
            ret = []
            label_to_category_id_map = self.get_label_to_category_id_map()

            for f in self.list_annotations():
                data = util.load_json(f)

                for i, shape in enumerate(data['shapes']):
                    if i % 2 == 0:
                        d = {
                            'area': None,
                            'bbox': self.get_annotation_bbox(shape['points']),
                            'category_id': label_to_category_id_map[shape['label']],
                            'id': ann_id,
                            'image_id': self.get_image_id(f),
                            'iscrowd': 0,
                        }
                    else:
                        # every 2nd loop the annotation is complete, so add it
                        # to the return and increment the annotation id
                        d['segmentation'] = self.get_segmentation(shape['points'])
                        ret.append(d)
                        ann_id += 1
            self._annotations = ret
        return self._annotations

    def get_image_id(self, path):
        filename, _ = os.path.splitext(os.path.basename(path))
        return int(filename)

    def get_imageid_to_imageann(self):
        return {x['id']: x for x in self.get_images()}

    def get_imageid_to_ann(self):
        """
        Returns a dict where the key is an imageid and the value
        is a list of annotations for that image
        """
        imageid_to_anns = {}
        for img in self.get_images():
            imageid_to_anns[img['id']] = []

        for a in self.get_annotations():
            imageid_to_anns[a['image_id']].append(a)

        return imageid_to_anns

    def get_image_ids(self):
        "Returns a list of image ids"
        return list(self.get_imageid_to_ann())

    def get_category_id_to_name(self):
        return {x['id']: x['name'] for x in self.get_categories()}
