import os
import unittest

from mlearning import util
from tests import config


class UtilTests(unittest.TestCase):

    def test_load_json(self):
        ret = util.load_json(os.path.join(config.ANNOTATIONS_DIR, '1.json'))

        assert isinstance(ret, dict)
