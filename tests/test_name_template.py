#!/usr/bin/env python3
"""
@input  依赖：Pillow, SpriteSplitter
@output 导出：name template fallback tests
@pos    精灵命名模板为空时的回归测试入口

⚠️ 一旦本文件被更新，务必更新以上注释
"""

import os
import tempfile
import unittest

from PIL import Image

from sprite_splitter import SpriteSplitter, SpriteRect


class NameTemplateTests(unittest.TestCase):
    def test_empty_template_falls_back_to_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, "sheet.png")
            output_dir = os.path.join(temp_dir, "out")

            image = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
            image.save(image_path)

            splitter = SpriteSplitter(image_path)
            splitter.sprites = [
                SpriteRect(x=0, y=0, width=5, height=5, name="spriteA")
            ]
            splitter.save_sprites(output_dir, name_template="")

            output_path = os.path.join(output_dir, "spriteA.png")
            self.assertTrue(os.path.exists(output_path))


if __name__ == "__main__":
    unittest.main()
