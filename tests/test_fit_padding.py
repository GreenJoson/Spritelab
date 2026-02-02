#!/usr/bin/env python3
"""
@input  依赖：Pillow, SpriteSplitter
@output 导出：fit padding tests
@pos    等比缩放(fit)导出时透明补边的回归测试入口

⚠️ 一旦本文件被更新，务必更新以上注释
"""

import os
import tempfile
import unittest

from PIL import Image

from sprite_splitter import SpriteSplitter


class FitPaddingTests(unittest.TestCase):
    def test_fit_pads_to_target_top(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            Image.new("RGBA", (72, 55), (255, 0, 0, 255)).save(image_path)

            splitter = SpriteSplitter(image_path)
            with Image.open(image_path) as handle:
                img = handle.convert("RGBA")
                out = splitter._resize_image(
                    img, mode="fit", scale=1.0, target_width=75, target_height=75, origin_mode="top"
                )

            self.assertEqual(out.size, (75, 75))
            self.assertEqual(out.getpixel((0, 0))[3], 255)
            self.assertEqual(out.getpixel((0, 74))[3], 0)

    def test_fit_pads_to_target_bottom(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            Image.new("RGBA", (72, 55), (255, 0, 0, 255)).save(image_path)

            splitter = SpriteSplitter(image_path)
            with Image.open(image_path) as handle:
                img = handle.convert("RGBA")
                out = splitter._resize_image(
                    img, mode="fit", scale=1.0, target_width=75, target_height=75, origin_mode="bottom"
                )

            self.assertEqual(out.size, (75, 75))
            self.assertEqual(out.getpixel((0, 0))[3], 0)
            self.assertEqual(out.getpixel((0, 74))[3], 255)


if __name__ == "__main__":
    unittest.main()
