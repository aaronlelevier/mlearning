import os
import unittest

from tests import config
from mlearning.coco_checker import LabeledData


class CocoCheckerTests(unittest.TestCase):

    def test_all_images_numbered_sequentially(self):
        path = os.path.join(config.DATA_DIR, 'images-sequential-ok')

        ret_bool, ret_imgs = LabeledData.images_numbered_sequentially(path)

        assert ret_bool
        assert ret_imgs == []

    def test_not_all_images_numbered_sequentially(self):
        path = os.path.join(config.DATA_DIR, 'images-not-sequential')

        ret_bool, ret_imgs = LabeledData.images_numbered_sequentially(path)

        assert not ret_bool
        assert ret_imgs == [3, 4]
