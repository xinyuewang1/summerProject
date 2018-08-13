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

    # Test getFirstAndLastStop3
    def test_getFirstAndLastStop3(self):

        # Normal 1: 39a, 770, 793, lower case
        # should return 767, 7162, 4, 20
        self.assertEqual(getFirstAndLastStops3('39a', 770, 793), (767, 7162, 4, 20))

        # Normal 1: 39A, 770, 793, upper case
        self.assertEqual(getFirstAndLastStops3('39A', 770, 793), (767, 7162, 4, 20))

        # Abnormal 1, wrong order
        self.assertEqual(getFirstAndLastStops3('39a', 793, 770), (767, 7162, 4, 20))

        # Abnormal 2, not on the same path
        with self.assertRaises(FileNotFoundError):
            getFirstAndLastStops3('39a', 770, 766)

        # Abnormal 3, stops not on route
        with self.assertRaises(FileNotFoundError):
            getFirstAndLastStops3('someroute', 770, 793)

    # Test for class Ett39A
    def test_Ett39A(self):
        # test set
        ett = Ett39A('67', 1444, 3913, 0, 18, "16:45", 3, "7/26/2018")

        self.assertEqual(ett.timeInSec, 60300)

        # 16:45, afternoon peak
        self.assertEqual(ett.timeValue(), [0, 0, 0, 0, 1, 0, 0])

        # estimatedTime


