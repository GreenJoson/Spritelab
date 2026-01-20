#!/usr/bin/env python3
"""
@input  依赖：Pillow, SpriteSplitter
@output 导出：restore mode tests
@pos    精灵表还原尺寸的回归测试入口
 
⚠️ 一旦本文件被更新，务必更新以上注释
"""

import json
import os
import tempfile
import unittest

from PIL import Image

from sprite_splitter import SpriteSplitter


class RestoreModeTests(unittest.TestCase):
    def test_data_file_restore_source_size(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            data_path = os.path.join(temp_dir, "sheet.json")
            output_dir = os.path.join(temp_dir, "out")

            image = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
            for x in range(2, 6):
                for y in range(3, 8):
                    image.putpixel((x, y), (255, 0, 0, 255))
            image.save(image_path)

            data = {
                "file": "sheet.png",
                "frames": {
                    "spriteA": {
                        "x": 2,
                        "y": 3,
                        "w": 4,
                        "h": 5,
                        "offX": 1,
                        "offY": 2,
                        "sourceW": 8,
                        "sourceH": 9,
                    }
                },
            }
            with open(data_path, "w", encoding="utf-8") as handle:
                json.dump(data, handle)

            splitter = SpriteSplitter(image_path)
            splitter.split_by_data_file(data_path)
            splitter.save_sprites(output_dir)

            output_path = os.path.join(output_dir, "spriteA.png")
            self.assertTrue(os.path.exists(output_path))
            with Image.open(output_path) as output_image:
                self.assertEqual(output_image.size, (8, 9))


if __name__ == "__main__":
    unittest.main()
