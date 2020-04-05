import logging as log
from datetime import datetime
from unittest import TestCase

from backend_scripts.two_way_dict import TwoWayDict


class TestTwoWayDict(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTwoWayDict, self).__init__(*args, **kwargs)
        log.basicConfig(level=log.DEBUG)

    def test_insert(self):
        a = TwoWayDict()
        a[1] = datetime(2015, 1, 1)
        self.assertEqual(a.get(1), datetime(2015, 1, 1))
        self.assertEqual(a.get(datetime(2015, 1, 1)), 1)
        self.assertRaises(KeyError, lambda x: a[x], 7)
        self.assertRaises(KeyError, lambda x: a[x], datetime(2012, 1, 1))

        a[datetime(2012, 1, 1)] = 21
        self.assertEqual(a.get(21), datetime(2012, 1, 1))
        self.assertEqual(a.get(datetime(2012, 1, 1)), 21)
        self.assertRaises(KeyError, lambda x: a[x], 7)
        self.assertRaises(KeyError, lambda x: a[x], datetime(2013, 1, 1))

    def test_pop(self):
        a = TwoWayDict()
        a[1] = datetime(2015, 1, 1)
        a[2] = datetime(2020, 12, 31)
        a[datetime(2012, 1, 1)] = 75
        value_a = a.pop(2)
        self.assertEqual(value_a, datetime(2020, 12, 31))
        self.assertRaises(KeyError, lambda x: a[x], 2)
        self.assertRaises(KeyError, lambda x: a[x], datetime(2020, 12, 31))
        self.assertIsNotNone(a.get(1))

    def test_del(self):
        a = TwoWayDict()
        a[1] = datetime(2015, 1, 1)
        a[2] = datetime(2020, 12, 31)
        a[datetime(2012, 1, 1)] = 75
        del a[2]
        del a[datetime(2012, 1, 1)]
        self.assertRaises(KeyError, lambda x: a[x], 2)
        self.assertRaises(KeyError, lambda x: a[x], datetime(2012, 1, 1))
        self.assertRaises(KeyError, lambda x: a[x], 75)
        self.assertRaises(KeyError, lambda x: a[x], datetime(2020, 12, 31))
        self.assertIsNotNone(a.get(1))
