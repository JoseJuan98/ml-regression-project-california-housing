#!/usr/bin/env python
"""testTemplate.

Tests NumberList and FrequencyDistribution, classes for statistics.

Example of code use:

>>> from unittest import TestCase
>>> class TestClass(TestCase)
>>> # ...
"""
from unittest import TestCase, main


class NumberListTests(TestCase):  # must remember to subclass TestCase
    """Tests of the NumberList class."""

    def setUp(self):
        """Define a few standard NumberLists."""
        self.Null = None  # test empty init
        self.Empty = []  # test init with empty sequence
        self.Single = [5]  # single item
        self.Zero = [0]  # single, False item
        self.Three = [1, 2, 3]  # multiple items
        self.ZeroMean = [1, -1]  # items nonzero, mean zero
        self.ZeroVar = [1, 1, 1]  # items nonzero, mean nonzero, variance zero

        # etc. These objects shared by all tests, and created new each time a method
        # starting with the string 'test' is called (i.e. the same object does not
        # persist between tests: rather, you get separate copies).

        def test_mean_empty(self):
            """NumberList.mean() should raise ValueError on empty object"""
            for empty in (self.Null, self.Empty):
                self.assertRaises(ValueError, empty.mean)

        def test_mean_single(self):
            """NumberList.mean() should return item if only 1 item in list"""
            for single in (self.Single, self.Zero):
                self.assertEqual(single.mean(), single[0])

        # pipeline tests of mean

        def test_var_failures(self):
            """NumberList.var() should raise ZeroDivisionError if <2 items"""
            for small in (self.Null, self.Empty, self.Single, self.Zero):
                self.assertRaises(ZeroDivisionError, small.var)

        # pipeline tests of var
        # tests of pipeline methods


class FrequencyDistributionTests(TestCase):
    pass  # much code deleted


# tests of pipeline classes

if __name__ == "__main__":  # run tests if called from command-line
    main()
