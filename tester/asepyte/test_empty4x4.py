# -*- coding: utf-8 -*-

from unittest import TestCase, main

from asepyte import load
from asepyte.header import MAGIC_NUMBER
from tester.assets import get_assets_path


class Empty4x4TestCase(TestCase):
    def setUp(self):
        self.path = get_assets_path() / "empty4x4.aseprite"
        self.assertTrue(self.path.is_file())

    def test_default(self):
        with open(self.path, "rb") as f:
            aseprite = load(f)

        self.assertIsNotNone(aseprite)
        self.assertEqual(aseprite.header.magic_number, MAGIC_NUMBER)
        self.assertEqual(aseprite.header.frames, 1)


if __name__ == "__main__":
    main()
