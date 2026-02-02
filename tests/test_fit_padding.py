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
            img = Image.new("RGBA", (72, 55), (0, 0, 0, 0))
            # Put content near the bottom, leaving transparent top area
            for x in range(10, 62):
                for y in range(45, 55):
                    img.putpixel((x, y), (255, 0, 0, 255))
            img.save(image_path)

            splitter = SpriteSplitter(image_path)
            with Image.open(image_path) as handle:
                img = handle.convert("RGBA")
                out = splitter._resize_image(
                    img, mode="fit", scale=1.0, target_width=75, target_height=75, pad_align="top_left", pad_smart=True
                )

            self.assertEqual(out.size, (75, 75))
            # Smart top align: content should touch the top edge
            alpha = out.split()[-1]
            bbox = alpha.getbbox()
            self.assertIsNotNone(bbox)
            self.assertLessEqual(bbox[1], 1)
            # Bottom-most line should be transparent (content is only ~10px tall)
            self.assertEqual(out.getpixel((20, 74))[3], 0)

    def test_fit_pads_to_target_bottom(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            img = Image.new("RGBA", (72, 55), (0, 0, 0, 0))
            # Put content near the top, leaving transparent bottom area
            for x in range(10, 62):
                for y in range(0, 10):
                    img.putpixel((x, y), (255, 0, 0, 255))
            img.save(image_path)

            splitter = SpriteSplitter(image_path)
            with Image.open(image_path) as handle:
                img = handle.convert("RGBA")
                out = splitter._resize_image(
                    img, mode="fit", scale=1.0, target_width=75, target_height=75, pad_align="bottom_left", pad_smart=True
                )

            self.assertEqual(out.size, (75, 75))
            # Smart bottom align: content should touch the bottom edge
            alpha = out.split()[-1]
            bbox = alpha.getbbox()
            self.assertIsNotNone(bbox)
            self.assertGreaterEqual(bbox[3], 74)
            self.assertEqual(out.getpixel((20, 0))[3], 0)


if __name__ == "__main__":
    unittest.main()
