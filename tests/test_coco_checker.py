import os
import unittest
import pytest

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

    def test_bboxes_and_masks_all__ok(self):
        path = os.path.join(config.DATA_DIR, 'ann_label_ok')
        LabeledData.bboxes_and_masks_all(path)

    def test_bboxes_and_masks_all__raise_error_if_not_labeled_correctly(self):
        path = os.path.join(config.DATA_DIR, 'ann_label_not_ok')
        with pytest.raises(AssertionError):
            LabeledData.bboxes_and_masks_all(path)

    def test_bboxes_and_masks_order_ok(self):
        path = os.path.join(config.DATA_DIR, 'ann_label_ok.json')

        ret = LabeledData.bboxes_and_masks_correctly_ordered(path)

        assert ret == True

    def test_bboxes_and_masks_order_incorrect(self):
        path = os.path.join(config.DATA_DIR, 'ann_label_not_ok.json')

        with pytest.raises(AssertionError):
            LabeledData.bboxes_and_masks_correctly_ordered(path)
