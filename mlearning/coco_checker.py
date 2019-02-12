import json
from pathlib import Path


class LabeledData:

    @classmethod
    def images_numbered_sequentially(cls, filepath):
        """
        Returns a tuple (bool, list)

        The bool is if the images are sequentially numbered or not

        The list returned is the unsequential images for futher
        inspection
        """
        ret = True
        unseq_imgs = []

        path = Path(filepath)
        filenames = []
        for f in path.glob('**/*.jpg'):
            if f.is_file():
                name, ext = f.name.split('.')
                filenames.append(int(name))

        idx = None
        for f in sorted(filenames):
            if idx == None:
                idx = f
            else:
                if f != idx+1:
                    unseq_imgs.append(f)
                    ret = False
                idx += 1

        return ret, unseq_imgs

    @classmethod
    def bboxes_and_masks_all(cls, filepath):
        path = Path(filepath)
        for f in path.glob('**/*.json'):
            cls.bboxes_and_masks_correctly_ordered(f)

    @classmethod
    def bboxes_and_masks_correctly_ordered(cls, filepath):
        with open(filepath) as f:
            data = json.loads(f.read())

        assert data['shapes'][0]['label'] == 'car' and data['shapes'][0]['shape_type'] == 'rectangle'
        assert data['shapes'][1]['label'] == 'car' and data['shapes'][1]['shape_type'] == 'polygon'
        assert data['shapes'][2]['label'] == 'license' and data['shapes'][2]['shape_type'] == 'rectangle'
        assert data['shapes'][3]['label'] == 'license' and data['shapes'][3]['shape_type'] == 'polygon'

        return True
