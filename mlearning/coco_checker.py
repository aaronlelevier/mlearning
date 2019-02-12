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
