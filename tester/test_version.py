# -*- coding: utf-8 -*-

from unittest import TestCase, main

from asepyte import __version__


class VersionTestCase(TestCase):
    def test_version(self):
        version = tuple(map(lambda x: int(x), __version__.split(".")))
        self.assertGreaterEqual(version, (0, 0, 1))


if __name__ == "__main__":
    main()
