import unittest

import numpy as np


class BaseTestCase(unittest.TestCase):

    def assert_arr_equals(self, ret, raw_ret, msg=""):
        """
        User to assert arrays are equal when precision is an issue
        """
        error_msg = f"\nret:\n{ret}\nraw_ret:\n{raw_ret}"
        if msg:
            error_msg += f"\n{msg}"

        assert np.isclose(
                np.array(ret, dtype=np.float16),
                np.array(raw_ret, dtype=np.float16)
            ).all(), error_msg

    def assert_float_equals(self, ret, raw_ret, msg=""):
        """
        User to assert floats are equal when precision is an issue
        """
        def str_float(x):
            return "{:.8f}".format(x)

        if isinstance(ret, torch.Tensor):
            ret = ret.item()

        assert str_float(ret) == str_float(raw_ret), msg
