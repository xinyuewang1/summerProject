from django.test import TestCase
from busRoute.utils import *
import sys
import os
# sys.path.insert(0, "/path/to/parent/of/courseware") # /home/projects/my-djproj

from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

# import django
# django.setup()


class TestUtils(TestCase):

    # Test load_obj
    def test_load_obj(self):
        # Normal situation 1: name ends with pkl
        p1 = load_obj('pickles/39a1.pkl')
        self.assertTrue(p1)

        # Normal situation 2: enter basename
        self.assertTrue(load_obj('pickles/39a1'))

        # Abnormal 1: file doesn't exist
        self.assertRaises(FileNotFoundError, load_obj('pickles/something'))

        # Abnormal 2: directory doesn't exist
        self.assertRaises(FileNotFoundError, load_obj('some/thing'))

    def test_getFirstAndLastStop3(self):
        #