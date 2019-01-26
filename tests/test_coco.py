import os
import unittest

import numpy as np

from mlearning import coco
from tests import config
from tests.base import BaseTestCase


class AnnotationTests(BaseTestCase):

    def setUp(self):
        path = config.ANNOTATIONS_DIR

        self.ann = coco.Annotation(path)

    def test_init(self):
        assert os.path.isdir(self.ann.path)
        assert self.ann.path == \
            os.path.join(config.PROJECT_DIR, 'tests/data/annotations')

    def test_list_annotations(self):
        raw_ret = [
            os.path.join(config.ANNOTATIONS_DIR, '1.json'),
            os.path.join(config.ANNOTATIONS_DIR, '2.json'),
        ]

        ret = self.ann.list_annotations()

        assert ret == raw_ret

    def test_get_categories(self):
        raw_ret = [
            {'supercategory': 'license', 'id': 1, 'name': 'license'},
            {'supercategory': 'car', 'id': 2, 'name': 'car'},
        ]

        ret = self.ann.get_categories()

        assert ret == raw_ret

    def test_get_images(self):
        raw_ret = [
            {'id': 1, 'height': 450, 'width': 600, 'file_name': '1.jpg'},
            {'id': 2, 'height': 450, 'width': 600, 'file_name': '2.jpg'},
        ]

        ret = self.ann.get_images()

        assert ret == raw_ret

    def test_get_image_ann(self):
        raw_ret = {'id': 1, 'height': 450, 'width': 600, 'file_name': '1.jpg'}
        path = os.path.join(config.ANNOTATIONS_DIR, '1.json')

        ret = self.ann.get_image_ann(path)

        assert ret == raw_ret

    def test_get_annotation_bbox(self):
        labelme_bb = [[290, 386], [397, 433]]
        raw_ret = [290, 386, 107,  47]

        ret = self.ann.get_annotation_bbox(labelme_bb)

        assert ret == raw_ret

    def test_label_to_category_id_map(self):
        raw_ret = {
            'license': 1,
            'car': 2
        }

        ret = self.ann.label_to_category_id_map()

        assert ret == raw_ret

    def test_get_segmentation(self):
        labelme_seg = [[178, 252], [209, 258], [208, 280], [179, 274]]
        raw_ret = [[178, 252, 209, 258, 208, 280, 179, 274]]

        ret = self.ann.get_segmentation(labelme_seg)

        assert ret == raw_ret

    def test_get_annotations(self):
        raw_ret = [{
            'area': None,
            'bbox': [179, 252, 29, 28],
            'category_id': 1,
            'id': 1,
            'image_id': 1,
            'iscrowd': 0,
            'segmentation': [[178, 252, 209, 258, 208, 280, 179, 274]]
        },{
            'area': None,
            'bbox': [158, 137, 373, 182],
            'category_id': 2,
            'id': 2,
            'image_id': 1,
            'iscrowd': 0,
            'segmentation': [[
                254,
                180,
                313,
                142,
                407,
                133,
                476,
                139,
                519,
                174,
                529,
                187,
                530,
                226,
                510,
                270,
                484,
                270,
                396,
                298,
                379,
                317,
                345,
                319,
                327,
                305,
                281,
                306,
                164,
                282,
                153,
                237,
                184,
                204]]
        }]

        ret = self.ann.get_annotations()

        assert ret == raw_ret
