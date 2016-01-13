#!/usr/bin/env python

import unittest
from Ubuntu-Linux-Installer  import helpers

class HelpersTestCase(unittest.TestCase):
    def test_platform(self):
        self.assertFlase(helpers.is_linux())

if __name__ == '__main__':
    unittest.main()