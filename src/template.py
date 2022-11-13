#!/usr/bin/env python
"""Provides NumberList and FrequencyDistribution, classes for statistics.

NumberList holds a sequence of numbers, and defines several statistical
operations (mean, stdev, etc.) FrequencyDistribution holds a mapping from
items (not necessarily numbers) to counts, and defines operations such as
Shannon entropy and frequency normalization.
"""
# * Other example:

"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

        @Author: ...
        @Date: ....
        @Credit: ...
        @Links: ...
"""

# from math import sqrt, log, e
# from random import choice, random
# from Utils import indices

__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
               "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"


class NumberList(list):
    pass  # much code deleted


class FrequencyDistribution(dict):
    pass  # much code deleted


if __name__ == '__main__':  # code to execute if called from command-line
    pass  # do nothing - code deleted
# use this either for a simple example of how to use the module,
# or when the module can meaningfully be called as a script.


# Check [Docs Methods](http://epydoc.sourceforge.net/manual-fields.html#module-metadata-variables)

# Style 2:

# !/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
# ----------------------------------------------------------------------------
# Created By  : name_of_the_creator   Line 3
# Created Date: date/month/time ..etc
# version ='1.0'
# ---------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""  # Line 4
# ---------------------------------------------------------------------------
# Imports Line 5
# ---------------------------------------------------------------------------
# from ... import ...  #Line 6
