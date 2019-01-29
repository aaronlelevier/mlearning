import os

from mlearning import coco, util

from tests import config
from tests.base import BaseTestCase

TEST_IMAGES = [
    {'id': 1, 'height': 450, 'width': 600, 'file_name': '1.jpg'},
    {'id': 2, 'height': 450, 'width': 600, 'file_name': '2.jpg'},
]

TEST_CATEGORIES = [
    {'supercategory': 'license', 'id': 1, 'name': 'license'},
    {'supercategory': 'car', 'id': 2, 'name': 'car'},
]

TEST_ANNOTATIONS = [{
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
},{
    'area': None,
    'bbox': [124, 68, 423, 375],
    'category_id': 2,
    'id': 3,
    'image_id': 2,
    'iscrowd': 0,
    'segmentation': [[
        184, 155, 245, 68, 379, 76, 404, 91, 439, 145, 470, 147,
        474, 163, 453, 174, 525, 275, 528, 315, 546, 350, 518, 409,
        443, 441, 228, 437, 130, 392, 117, 335, 129, 281, 143, 224]]
},{
    'area': None,
    'bbox': [291, 386, 105, 44],
    'category_id': 1,
    'id': 4,
    'image_id': 2,
    'iscrowd': 0,
    'segmentation': [[298, 386, 394, 391, 388, 428, 292, 427]]
}]


class AnnotationTests(BaseTestCase):

    def setUp(self):
        self.ann = coco.Annotation(
            path=os.path.join(config.PROJECT_DIR, 'tests/data'))

    def test_init(self):
        assert os.path.isdir(self.ann.ann_path)
        assert self.ann.ann_path == \
            os.path.join(config.PROJECT_DIR, 'tests/data/annotations')
        assert self.ann.image_path == \
            os.path.join(config.PROJECT_DIR, 'tests/data/images')
        assert self.ann.output_path == \
            os.path.join(config.PROJECT_DIR, 'tests/data/output')

    def test_all(self):
        ret = self.ann.all()

        assert isinstance(ret, dict)
        assert len(ret) == 5
        # info
        assert isinstance(ret['info'], dict)
        # images
        assert isinstance(ret['images'], list)
        assert ret['images'] == TEST_IMAGES
        # licenses
        assert isinstance(ret['licenses'], list)
        # annotations
        assert isinstance(ret['annotations'], list)
        assert ret['annotations'] == TEST_ANNOTATIONS
        # categories
        assert isinstance(ret['categories'], list)
        assert ret['categories'] == TEST_CATEGORIES

    def test_generate(self):
        # rm file file if present
        output_path = os.path.join(config.OUTPUT_DIR, 'annotations.json')
        if os.path.isfile(output_path):
            os.remove(output_path)
        assert not os.path.isfile(output_path)

        self.ann.generate(output_path)

        assert os.path.isfile(output_path)
        data = util.load_json(output_path)
        assert data == self.ann.all()
        # cleanup file when done
        os.remove(output_path)

    def test_list_annotations(self):
        raw_ret = [
            os.path.join(config.ANNOTATIONS_DIR, '1.json'),
            os.path.join(config.ANNOTATIONS_DIR, '2.json'),
        ]

        ret = self.ann.list_annotations()

        assert ret == raw_ret

    def test_get_categories(self):
        raw_ret = TEST_CATEGORIES

        ret = self.ann.get_categories()

        assert ret == raw_ret

    def test_get_images(self):
        raw_ret = TEST_IMAGES

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

    def test_get_label_to_category_id_map(self):
        raw_ret = {
            'license': 1,
            'car': 2
        }

        ret = self.ann.get_label_to_category_id_map()

        assert ret == raw_ret

    def test_get_segmentation(self):
        labelme_seg = [[178, 252], [209, 258], [208, 280], [179, 274]]
        raw_ret = [[178, 252, 209, 258, 208, 280, 179, 274]]

        ret = self.ann.get_segmentation(labelme_seg)

        assert ret == raw_ret

    def test_get_annotations(self):
        raw_ret = TEST_ANNOTATIONS

        ret = self.ann.get_annotations()

        assert ret == raw_ret

    def test_get_imageid_to_imageann(self):
        ret = self.ann.get_imageid_to_imageann()

        assert isinstance(ret, dict)
        assert ret == {
            1: TEST_IMAGES[0],
            2: TEST_IMAGES[1]
        }

    def test_get_imageid_to_ann(self):
        ret = self.ann.get_imageid_to_ann()

        assert isinstance(ret, dict)
        assert ret == {
            1: TEST_ANNOTATIONS[:2],
            2: TEST_ANNOTATIONS[2:]
        }

    def test_get_image_ids(self):
        ret = self.ann.get_image_ids()

        assert ret == [1, 2]

    def test_get_category_id_to_name(self):
        ret = self.ann.get_category_id_to_name()

        assert ret == {
            1: 'license',
            2: 'car'
        }
