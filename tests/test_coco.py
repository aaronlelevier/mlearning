import os
import unittest

from mlearning import coco
from tests import config


class AnnotationTests(unittest.TestCase):

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

    # def test_get_annotation(self):
