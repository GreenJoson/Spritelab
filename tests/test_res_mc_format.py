#!/usr/bin/env python3
"""
@input  依赖：Pillow, SpriteSplitter
@output 导出：res/mc JSON format tests
@pos    res/mc 格式解析回归测试入口

⚠️ 一旦本文件被更新，务必更新以上注释
"""

import json
import os
import tempfile
import unittest

from PIL import Image

from sprite_splitter import SpriteSplitter


class ResMcFormatTests(unittest.TestCase):
    def test_res_mc_format_parses_frames(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            data_path = os.path.join(temp_dir, "sheet.json")

            Image.new("RGBA", (32, 32), (0, 0, 0, 0)).save(image_path)

            data = {
                "res": {
                    "A1": {"x": 0, "y": 0, "w": 8, "h": 8},
                    "B2": {"x": 8, "y": 0, "w": 8, "h": 8}
                },
                "mc": {
                    "pigGif": {
                        "frameRate": 24,
                        "frames": [
                            {"res": "A1", "x": 2, "y": 3},
                            {"res": "B2", "x": 1, "y": 4}
                        ]
                    }
                }
            }

            with open(data_path, "w", encoding="utf-8") as handle:
                json.dump(data, handle)

            splitter = SpriteSplitter(image_path)
            sprites = splitter.split_by_data_file(data_path)

            self.assertEqual(len(sprites), 2)
            self.assertEqual(sprites[0].name, "pigGif_0")
            self.assertEqual(sprites[1].name, "pigGif_1")
            if splitter.image:
                splitter.image.close()


if __name__ == "__main__":
    unittest.main()
