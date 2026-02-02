#!/usr/bin/env python3
"""
@input  依赖：Pillow, i18n
@output 导出：SpriteSplitter, SpriteRect
@pos    精灵表拆分的核心逻辑（含导出批量缩放：fit 等比缩放 + 透明补边）

⚠️ 一旦本文件被更新，务必更新以上注释

精灵表拆分器 (Sprite Sheet Splitter)
模仿TexturePacker的功能实现的简易版本

功能：
1. Grid模式 - 按固定网格拆分
2. Rectangular模式 - 自动检测矩形区域（通过透明像素边界）
3. Data File模式 - 使用JSON数据文件拆分

作者: AI Assistant
日期: 2024
"""

import os
import json
import argparse
from PIL import Image
from dataclasses import dataclass
from i18n import i18n
from typing import List, Tuple, Optional, Dict
from pathlib import Path


def resolve_image_path_from_data_file(data_path: str) -> Optional[str]:
    """根据JSON数据文件尝试解析对应的精灵表图片路径"""
    if not os.path.exists(data_path):
        return None

    try:
        with open(data_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
    except Exception:
        return None

    file_name = data.get("file")
    if not file_name:
        meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
        file_name = meta.get("image") or meta.get("imagePath")

    if not file_name:
        return None

    data_dir = Path(data_path).parent
    candidate = Path(file_name)
    if not candidate.is_absolute():
        candidate = data_dir / candidate

    if candidate.exists():
        return str(candidate)

    if Path(file_name).exists():
        return str(Path(file_name))

    return None


@dataclass
class SpriteRect:
    """精灵矩形区域"""
    x: int
    y: int
    width: int
    height: int
    name: str = ""
    off_x: int = 0
    off_y: int = 0
    source_w: int = 0
    source_h: int = 0


class SpriteSplitter:
    """精灵表拆分器主类"""

    def __init__(self, image_path: str):
        """
        初始化拆分器

        Args:
            image_path: 精灵表图片路径
        """
        self.image_path = image_path
        self.image: Optional[Image.Image] = None
        self.sprites: List[SpriteRect] = []
        self.restore_source = False
        self.offset_origin = "top"
        self._load_image()

    def _load_image(self):
        """加载图片"""
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"找不到图片文件: {self.image_path}")

        # Pillow 会延迟读取像素数据；这里强制加载并断开文件句柄，避免导出/测试阶段资源泄漏
        with Image.open(self.image_path) as handle:
            if handle.mode != "RGBA":
                loaded = handle.convert("RGBA")
            else:
                loaded = handle.copy()
            loaded.load()
            self.image = loaded

        print(f"✓ 已加载图片: {self.image_path}")
        print(f"  尺寸: {self.image.width} x {self.image.height}")
        print(f"  模式: {self.image.mode}")

    @staticmethod
    def _safe_int(value, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _extract_frame_data(self, frame_data: Dict) -> Tuple[int, int, int, int, int, int, int, int]:
        frame = frame_data.get('frame', frame_data)
        x = self._safe_int(frame.get('x', 0))
        y = self._safe_int(frame.get('y', 0))
        width = self._safe_int(frame.get('w', frame.get('width', 0)))
        height = self._safe_int(frame.get('h', frame.get('height', 0)))

        sprite_source = frame_data.get('spriteSourceSize') if isinstance(frame_data.get('spriteSourceSize'), dict) else {}
        off_x = self._safe_int(sprite_source.get('x', frame_data.get('offX', frame_data.get('offsetX', 0))))
        off_y = self._safe_int(sprite_source.get('y', frame_data.get('offY', frame_data.get('offsetY', 0))))

        source_size = frame_data.get('sourceSize') if isinstance(frame_data.get('sourceSize'), dict) else {}
        source_w = self._safe_int(source_size.get('w', source_size.get('width', frame_data.get('sourceW', frame_data.get('sourceWidth', 0)))))
        source_h = self._safe_int(source_size.get('h', source_size.get('height', frame_data.get('sourceH', frame_data.get('sourceHeight', 0)))))

        return x, y, width, height, off_x, off_y, source_w, source_h

    def split_by_grid(
        self,
        columns: int = 0,
        rows: int = 0,
        sprite_width: int = 0,
        sprite_height: int = 0,
        padding: int = 0,
        margin: int = 0
    ) -> List[SpriteRect]:
        """
        Grid模式 - 按固定网格拆分

        可以指定列数和行数，或者指定单个精灵的宽高

        Args:
            columns: 列数 (可选)
            rows: 行数 (可选)
            sprite_width: 精灵宽度 (可选)
            sprite_height: 精灵高度 (可选)
            padding: 精灵之间的间距
            margin: 边缘间距

        Returns:
            精灵矩形列表
        """
        if not self.image:
            raise ValueError("请先加载图片")

        self.restore_source = False
        img_width = self.image.width
        img_height = self.image.height

        # 计算有效区域（去除边缘间距）
        effective_width = img_width - 2 * margin
        effective_height = img_height - 2 * margin

        # 根据给定参数计算网格
        if sprite_width > 0 and sprite_height > 0:
            # 根据精灵尺寸计算列数和行数
            columns = (effective_width + padding) // (sprite_width + padding)
            rows = (effective_height + padding) // (sprite_height + padding)
        elif columns > 0 and rows > 0:
            # 根据列数行数计算精灵尺寸
            sprite_width = (effective_width - padding * (columns - 1)) // columns
            sprite_height = (effective_height - padding * (rows - 1)) // rows
        else:
            raise ValueError("请指定 columns/rows 或 sprite_width/sprite_height")

        print(f"\n📐 Grid模式拆分:")
        print(f"  网格: {columns} 列 x {rows} 行")
        print(f"  精灵尺寸: {sprite_width} x {sprite_height}")
        print(f"  间距: {padding}, 边缘: {margin}")

        self.sprites = []
        sprite_index = 0

        for row in range(rows):
            for col in range(columns):
                x = margin + col * (sprite_width + padding)
                y = margin + row * (sprite_height + padding)

                sprite = SpriteRect(
                    x=x,
                    y=y,
                    width=sprite_width,
                    height=sprite_height,
                    name=f"sprite_{sprite_index:04d}"
                )
                self.sprites.append(sprite)
                sprite_index += 1

        print(f"  共检测到 {len(self.sprites)} 个精灵")
        return self.sprites

    def split_by_rectangle(
        self,
        min_width: int = 1,
        min_height: int = 1,
        alpha_threshold: int = 0
    ) -> List[SpriteRect]:
        """
        Rectangular模式 - 自动检测精灵区域

        智能检测：自动识别背景色（透明或纯色），然后检测非背景区域

        Args:
            min_width: 最小精灵宽度
            min_height: 最小精灵高度
            alpha_threshold: alpha阈值，低于此值视为透明

        Returns:
            精灵矩形列表
        """
        if not self.image:
            raise ValueError("请先加载图片")

        self.restore_source = False
        print(f"\n🔍 Rectangular模式拆分:")
        print(f"  最小尺寸: {min_width} x {min_height}")
        print(f"  Alpha阈值: {alpha_threshold}")

        # 获取像素数据
        if self.image.mode != 'RGBA':
            img = self.image.convert('RGBA')
        else:
            img = self.image

        pixels = img.load()
        width, height = img.size

        # 智能检测背景色 - 从四个角采样
        corner_samples = [
            pixels[0, 0],
            pixels[width-1, 0],
            pixels[0, height-1],
            pixels[width-1, height-1]
        ]

        # 检测是否有透明背景
        has_transparent_bg = any(c[3] <= alpha_threshold for c in corner_samples)

        if has_transparent_bg:
            print("  检测到透明背景")
            bg_color = None
        else:
            # 找到最常见的角落颜色作为背景色
            from collections import Counter
            # 只比较RGB，忽略少许差异
            def color_key(c):
                return (c[0] // 10, c[1] // 10, c[2] // 10)

            color_counts = Counter(color_key(c) for c in corner_samples)
            most_common = color_counts.most_common(1)[0][0]

            # 从角落采样中找到最接近的实际颜色
            for c in corner_samples:
                if color_key(c) == most_common:
                    bg_color = c[:3]
                    break

            print(f"  检测到纯色背景: RGB{bg_color}")

        # 定义背景检测函数
        color_tolerance = 30  # 颜色容差

        def is_background(x: int, y: int) -> bool:
            """检查像素是否是背景"""
            if x < 0 or x >= width or y < 0 or y >= height:
                return True
            pixel = pixels[x, y]

            # 检查透明度
            if pixel[3] <= alpha_threshold:
                return True

            # 如果有非透明背景色，检查颜色是否接近背景
            if bg_color:
                diff = sum(abs(pixel[i] - bg_color[i]) for i in range(3))
                return diff < color_tolerance * 3

            return False

        # 创建访问标记矩阵
        visited = [[False] * width for _ in range(height)]

        def find_sprite_bounds(start_x: int, start_y: int) -> Optional[SpriteRect]:
            """从起始点找到精灵的边界"""
            if visited[start_y][start_x] or is_background(start_x, start_y):
                return None

            # 使用洪水填充找到连通区域的边界
            min_x, max_x = start_x, start_x
            min_y, max_y = start_y, start_y

            stack = [(start_x, start_y)]
            pixel_count = 0

            while stack:
                x, y = stack.pop()

                if x < 0 or x >= width or y < 0 or y >= height:
                    continue
                if visited[y][x] or is_background(x, y):
                    continue

                visited[y][x] = True
                pixel_count += 1
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

                # 4方向扩展
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

            sprite_width = max_x - min_x + 1
            sprite_height = max_y - min_y + 1

            # 检查尺寸和像素密度
            if sprite_width >= min_width and sprite_height >= min_height:
                # 检查区域内像素密度，过滤噪点
                area = sprite_width * sprite_height
                density = pixel_count / area
                if density > 0.01:  # 至少1%的填充率
                    return SpriteRect(
                        x=min_x,
                        y=min_y,
                        width=sprite_width,
                        height=sprite_height
                    )
            return None

        self.sprites = []
        sprite_index = 0

        # 扫描整个图片
        for y in range(height):
            for x in range(width):
                sprite = find_sprite_bounds(x, y)
                if sprite:
                    sprite.name = f"sprite_{sprite_index:04d}"
                    self.sprites.append(sprite)
                    sprite_index += 1

        # 按位置排序（从上到下，从左到右）
        self.sprites.sort(key=lambda s: (s.y, s.x))

        # 重新命名
        for i, sprite in enumerate(self.sprites):
            sprite.name = f"sprite_{i:04d}"

        print(f"  共检测到 {len(self.sprites)} 个精灵")
        return self.sprites

    def split_by_data_file(self, data_path: str) -> List[SpriteRect]:
        """
        Data File模式 - 使用JSON数据文件拆分

        支持的格式:
        - TexturePacker JSON格式
        - 通用JSON格式 (frames数组)

        Args:
            data_path: JSON数据文件路径

        Returns:
            精灵矩形列表
        """
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"找不到数据文件: {data_path}")

        print(f"\n📄 Data File模式拆分:")
        print(f"  数据文件: {data_path}")

        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.sprites = []
        has_restore_data = False

        # 尝试解析TexturePacker格式
        if 'frames' in data:
            frames = data['frames']

            # TexturePacker hash格式
            if isinstance(frames, dict):
                for name, frame_data in frames.items():
                    x, y, width, height, off_x, off_y, source_w, source_h = self._extract_frame_data(frame_data)
                    sprite = SpriteRect(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        name=name,
                        off_x=off_x,
                        off_y=off_y,
                        source_w=source_w,
                        source_h=source_h
                    )
                    if source_w > 0 and source_h > 0:
                        has_restore_data = True
                    self.sprites.append(sprite)

            # TexturePacker array格式
            elif isinstance(frames, list):
                for frame_data in frames:
                    name = frame_data.get('filename', frame_data.get('name', ''))
                    x, y, width, height, off_x, off_y, source_w, source_h = self._extract_frame_data(frame_data)
                    sprite = SpriteRect(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        name=name,
                        off_x=off_x,
                        off_y=off_y,
                        source_w=source_w,
                        source_h=source_h
                    )
                    if source_w > 0 and source_h > 0:
                        has_restore_data = True
                    self.sprites.append(sprite)

        # 尝试解析简单的sprites数组格式
        elif 'sprites' in data:
            for sprite_data in data['sprites']:
                x = self._safe_int(sprite_data.get('x', 0))
                y = self._safe_int(sprite_data.get('y', 0))
                width = self._safe_int(sprite_data.get('width', sprite_data.get('w', 0)))
                height = self._safe_int(sprite_data.get('height', sprite_data.get('h', 0)))
                off_x = self._safe_int(sprite_data.get('offX', sprite_data.get('offsetX', 0)))
                off_y = self._safe_int(sprite_data.get('offY', sprite_data.get('offsetY', 0)))
                source_w = self._safe_int(sprite_data.get('sourceW', sprite_data.get('sourceWidth', 0)))
                source_h = self._safe_int(sprite_data.get('sourceH', sprite_data.get('sourceHeight', 0)))

                sprite = SpriteRect(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    name=sprite_data.get('name', ''),
                    off_x=off_x,
                    off_y=off_y,
                    source_w=source_w,
                    source_h=source_h
                )
                if source_w > 0 and source_h > 0:
                    has_restore_data = True
                self.sprites.append(sprite)

        # 尝试解析 res/mc 格式（部分引擎导出的动画精灵表）
        elif isinstance(data.get('res'), dict):
            res_map = data.get('res', {})
            mc_map = data.get('mc') if isinstance(data.get('mc'), dict) else None

            if mc_map:
                for mc_name, mc_data in mc_map.items():
                    frames = mc_data.get('frames', []) if isinstance(mc_data, dict) else []
                    if not isinstance(frames, list):
                        continue
                    for index, frame in enumerate(frames):
                        if not isinstance(frame, dict):
                            continue
                        res_id = frame.get('res')
                        rect = res_map.get(res_id) if res_id else None
                        if not isinstance(rect, dict):
                            continue
                        x = self._safe_int(rect.get('x', 0))
                        y = self._safe_int(rect.get('y', 0))
                        width = self._safe_int(rect.get('w', rect.get('width', 0)))
                        height = self._safe_int(rect.get('h', rect.get('height', 0)))
                        off_x = self._safe_int(frame.get('x', 0))
                        off_y = self._safe_int(frame.get('y', 0))
                        sprite = SpriteRect(
                            x=x,
                            y=y,
                            width=width,
                            height=height,
                            name=f"{mc_name}_{index}",
                            off_x=off_x,
                            off_y=off_y
                        )
                        self.sprites.append(sprite)
            else:
                for res_id, rect in res_map.items():
                    if not isinstance(rect, dict):
                        continue
                    x = self._safe_int(rect.get('x', 0))
                    y = self._safe_int(rect.get('y', 0))
                    width = self._safe_int(rect.get('w', rect.get('width', 0)))
                    height = self._safe_int(rect.get('h', rect.get('height', 0)))
                    sprite = SpriteRect(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        name=str(res_id)
                    )
                    self.sprites.append(sprite)

        else:
            raise ValueError("不支持的JSON格式")

        self.restore_source = has_restore_data

        print(f"  共解析到 {len(self.sprites)} 个精灵")
        return self.sprites

    def _restore_sprite(self, sprite_img: Image.Image, sprite: SpriteRect, origin_mode: str) -> Image.Image:
        if sprite.source_w <= 0 or sprite.source_h <= 0:
            return sprite_img

        canvas = Image.new("RGBA", (sprite.source_w, sprite.source_h), (0, 0, 0, 0))
        offset_x = max(0, sprite.off_x)

        if origin_mode == "bottom":
            offset_y = max(0, sprite.source_h - sprite.off_y - sprite.height)
        else:
            offset_y = max(0, sprite.off_y)

        canvas.paste(sprite_img, (offset_x, offset_y), sprite_img)
        return canvas

    def save_sprites(
        self,
        output_dir: str,
        name_template: str = "{name}",
        format: str = "png",
        trim: bool = False,
        edge_crop: int = 0,
        smart_edge_detect: bool = False,
        remove_bg: bool = False,
        resize_mode: str = "none",
        resize_scale: float = 1.0,
        resize_width: int = 0,
        resize_height: int = 0,
        restore_source: Optional[bool] = None,
        offset_origin: Optional[str] = None
    ) -> List[str]:
        """
        保存拆分后的精灵图片

        Args:
            output_dir: 输出目录
            name_template: 命名模板，支持 {name}, {index}, {x}, {y}, {width}, {height}
            format: 输出格式 (png, jpg, webp等)
            trim: 是否裁剪透明边缘
            edge_crop: 边缘裁剪像素数（上下左右各裁剪N像素）
            smart_edge_detect: 智能边缘检测，自动移除边缘纯色分隔线
            remove_bg: 智能去除边缘纯色背景
            resize_mode: 缩放模式 - "none"(不缩放), "scale"(按比例), "width"(固定宽度), "height"(固定高度), "custom"(自定义), "fit"(等比适应并透明补边到目标尺寸)
            resize_scale: 缩放比例 (当resize_mode为"scale"时使用)
            resize_width: 目标宽度 (当resize_mode为"width"或"custom"时使用)
            resize_height: 目标高度 (当resize_mode为"height"或"custom"时使用)
            restore_source: 是否还原原始尺寸（offX/offY/sourceW/sourceH）
            offset_origin: 偏移原点（"top" 或 "bottom"）

        Returns:
            保存的文件路径列表
        """
        if not self.image:
            raise ValueError("请先加载图片")

        if not self.sprites:
            raise ValueError("请先执行拆分操作")

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n💾 保存精灵图片:")
        print(f"  输出目录: {output_dir}")
        print(f"  命名模板: {name_template}")
        print(f"  格式: {format}")
        print(f"  裁剪透明边缘: {trim}")
        print(f"  边缘裁剪: {edge_crop}px")
        print(f"  智能边缘检测: {smart_edge_detect}")
        print(f"  还原原始尺寸: {self.restore_source if restore_source is None else restore_source}")

        saved_files = []
        restore_active = self.restore_source if restore_source is None else restore_source
        origin_mode = (offset_origin or self.offset_origin or "top").lower()

        trim_active = trim
        edge_crop_active = edge_crop
        smart_edge_active = smart_edge_detect
        remove_bg_active = remove_bg

        if restore_active and (trim or edge_crop > 0 or smart_edge_detect or remove_bg):
            print("  ⚠️ 还原原始尺寸已开启，已忽略裁剪/去背景相关参数")
            trim_active = False
            edge_crop_active = 0
            smart_edge_active = False
            remove_bg_active = False

        if not name_template.strip():
            name_template = "{name}"

        for index, sprite in enumerate(self.sprites):
            # 裁剪精灵区域
            sprite_img = self.image.crop((
                sprite.x,
                sprite.y,
                sprite.x + sprite.width,
                sprite.y + sprite.height
            ))

            # 边缘裁剪（方案2）- 固定像素数裁剪
            if edge_crop_active > 0:
                w, h = sprite_img.size
                left = min(edge_crop_active, w // 2)
                top = min(edge_crop_active, h // 2)
                right = max(0, w - edge_crop_active)
                bottom = max(0, h - edge_crop_active)
                if right > left and bottom > top:
                    sprite_img = sprite_img.crop((left, top, right, bottom))

            # 智能边缘检测（方案3）- 自动检测并移除边缘纯色分隔线
            if smart_edge_active:
                sprite_img = self._smart_crop_edges(sprite_img)

            # 智能去除边缘背景 - 从边缘开始去除纯色背景
            if remove_bg_active:
                sprite_img = self._remove_edge_background(sprite_img)

            # 裁剪透明边缘
            if trim_active:
                bbox = sprite_img.getbbox()
                if bbox:
                    sprite_img = sprite_img.crop(bbox)

            # 还原原始尺寸（基于offX/offY/sourceW/sourceH）
            if restore_active and sprite.source_w > 0 and sprite.source_h > 0:
                sprite_img = self._restore_sprite(sprite_img, sprite, origin_mode)

            # 批量调整大小
            if resize_mode != "none" and sprite_img.size[0] > 0 and sprite_img.size[1] > 0:
                sprite_img = self._resize_image(
                    sprite_img, resize_mode, resize_scale, resize_width, resize_height, origin_mode
                )

            # 生成文件名 - 使用手动替换以支持更灵活的模板
            # 支持: {name}, {index}, {x}, {y}, {width}, {height}
            filename = name_template
            filename = filename.replace('{name}', sprite.name)
            filename = filename.replace('{index}', str(index))
            filename = filename.replace('{x}', str(sprite.x))
            filename = filename.replace('{y}', str(sprite.y))
            filename = filename.replace('{width}', str(sprite.width))
            filename = filename.replace('{height}', str(sprite.height))

            # 如果模板中没有任何变量，则添加索引以避免文件名冲突
            if filename == name_template and '{' not in filename:
                filename = f"{filename}_{index}"

            # 确保有正确的扩展名
            if not filename.lower().endswith(f'.{format}'):
                filename = f"{filename}.{format}"

            # 保存
            filepath = os.path.join(output_dir, filename)

            # 如果是jpg格式，需要转换为RGB
            if format.lower() in ['jpg', 'jpeg']:
                # 创建白色背景
                background = Image.new('RGB', sprite_img.size, (255, 255, 255))
                if sprite_img.mode == 'RGBA':
                    background.paste(sprite_img, mask=sprite_img.split()[3])
                else:
                    background.paste(sprite_img)
                background.save(filepath, quality=95)
            else:
                sprite_img.save(filepath)

            saved_files.append(filepath)

        print(f"  ✓ 已保存 {len(saved_files)} 个精灵图片")
        return saved_files

    def _smart_crop_edges(self, img: Image.Image, tolerance: int = 30) -> Image.Image:
        """
        智能边缘检测 - 自动移除边缘的纯色分隔线

        检测图片四边是否有连续的纯色（通常是白色分隔线），
        如果有则裁剪掉。

        Args:
            img: 输入图片
            tolerance: 颜色容差，判断是否为"纯色"的阈值

        Returns:
            裁剪后的图片
        """
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        pixels = img.load()
        width, height = img.size

        def is_uniform_color(line_pixels: list, tolerance: int) -> bool:
            """检查一行/列像素是否为均匀颜色（可能是分隔线）"""
            if not line_pixels:
                return False
            first_color = line_pixels[0]
            for pixel in line_pixels:
                for i in range(3):  # RGB通道
                    if abs(pixel[i] - first_color[i]) > tolerance:
                        return False
            return True

        def is_light_color(color: tuple) -> bool:
            """检查是否为浅色（白色或接近白色）"""
            if len(color) >= 3:
                return (color[0] + color[1] + color[2]) / 3 > 200
            return False

        crop_top = 0
        crop_bottom = 0
        crop_left = 0
        crop_right = 0

        # 检测顶部边缘
        for y in range(min(10, height)):
            row_pixels = [pixels[x, y] for x in range(width)]
            if is_uniform_color(row_pixels, tolerance) and is_light_color(row_pixels[0]):
                crop_top = y + 1
            else:
                break

        # 检测底部边缘
        for y in range(height - 1, max(height - 11, -1), -1):
            row_pixels = [pixels[x, y] for x in range(width)]
            if is_uniform_color(row_pixels, tolerance) and is_light_color(row_pixels[0]):
                crop_bottom = height - y
            else:
                break

        # 检测左边缘
        for x in range(min(10, width)):
            col_pixels = [pixels[x, y] for y in range(height)]
            if is_uniform_color(col_pixels, tolerance) and is_light_color(col_pixels[0]):
                crop_left = x + 1
            else:
                break

        # 检测右边缘
        for x in range(width - 1, max(width - 11, -1), -1):
            col_pixels = [pixels[x, y] for y in range(height)]
            if is_uniform_color(col_pixels, tolerance) and is_light_color(col_pixels[0]):
                crop_right = width - x
            else:
                break

        left = crop_left
        top = crop_top
        right = width - crop_right
        bottom = height - crop_bottom

        if right > left and bottom > top:
            return img.crop((left, top, right, bottom))

        return img

    def _resize_image(
        self,
        img: Image.Image,
        mode: str,
        scale: float,
        target_width: int,
        target_height: int,
        origin_mode: str = "top",
    ) -> Image.Image:
        """
        调整图像大小

        Args:
            img: 输入图片
            mode: 缩放模式 - "scale"(按比例), "width"(固定宽度), "height"(固定高度), "custom"(自定义), "fit"(等比适应并补边)
            scale: 缩放比例 (0.5 = 50%, 2.0 = 200%)
            target_width: 目标宽度
            target_height: 目标高度
            origin_mode: 贴图原点（"top" 或 "bottom"），用于fit模式的透明补边对齐

        Returns:
            调整大小后的图片
        """
        orig_width, orig_height = img.size

        if mode == "scale" and scale > 0:
            # 按比例缩放
            new_width = int(orig_width * scale)
            new_height = int(orig_height * scale)

        elif mode == "width" and target_width > 0:
            # 固定宽度，保持宽高比
            ratio = target_width / orig_width
            new_width = target_width
            new_height = int(orig_height * ratio)

        elif mode == "height" and target_height > 0:
            # 固定高度，保持宽高比
            ratio = target_height / orig_height
            new_width = int(orig_width * ratio)
            new_height = target_height

        elif mode == "custom" and target_width > 0 and target_height > 0:
            # 自定义尺寸（不保持宽高比）
            new_width = target_width
            new_height = target_height

        elif mode == "fit" and target_width > 0 and target_height > 0:
            # 适应尺寸（保持宽高比）并透明补边到固定画布尺寸，避免导出帧一高一矮
            ratio = min(target_width / orig_width, target_height / orig_height)
            new_width = min(target_width, int(orig_width * ratio))
            new_height = min(target_height, int(orig_height * ratio))

        else:
            # 无效参数，返回原图
            return img

        # 确保最小尺寸为1
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        # 使用高质量缩放
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # fit模式：补透明边到目标画布（输出严格等于target_width/target_height）
        if mode == "fit":
            if resized.size == (target_width, target_height):
                return resized

            if resized.mode != "RGBA":
                resized = resized.convert("RGBA")

            canvas = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
            paste_x = 0

            if origin_mode == "bottom":
                paste_y = max(0, target_height - resized.size[1])
            else:
                paste_y = 0

            canvas.paste(resized, (paste_x, paste_y), resized)
            return canvas

        return resized

    def _remove_edge_background(self, img: Image.Image, tolerance: int = 30) -> Image.Image:
        """
        智能去除边缘背景 - 从边缘开始去除纯色背景

        使用洪水填充算法，从图片四个边缘开始，将与边缘颜色相近的像素设为透明。
        只影响从边缘连通的区域，不会影响图像内部的相同颜色。

        Args:
            img: 输入图片
            tolerance: 颜色容差，用于判断是否为"相同颜色"

        Returns:
            去除背景后的图片
        """
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 复制图片以避免修改原图
        result = img.copy()
        pixels = result.load()
        width, height = result.size

        # 检测背景色 - 从四个角取样
        corner_colors = [
            pixels[0, 0],                      # 左上
            pixels[width-1, 0],                # 右上
            pixels[0, height-1],               # 左下
            pixels[width-1, height-1]          # 右下
        ]

        # 找到最常见的角落颜色作为背景色
        def color_distance(c1, c2):
            """计算两个颜色之间的距离"""
            return sum(abs(c1[i] - c2[i]) for i in range(3))

        # 简单起见，使用左上角颜色作为背景色
        # 如果四个角颜色相近，则使用平均值
        bg_color = corner_colors[0][:3]  # 只取RGB

        # 检查四个角是否颜色相近
        similar_corners = 0
        for color in corner_colors:
            if color_distance(color, bg_color) < tolerance * 3:
                similar_corners += 1

        if similar_corners < 2:
            # 角落颜色不一致，可能不是纯色背景，直接返回
            return img

        def colors_match(c1, c2, tol):
            """检查两个颜色是否相近"""
            return all(abs(c1[i] - c2[i]) <= tol for i in range(3))

        # 使用BFS从边缘开始填充
        visited = [[False] * width for _ in range(height)]
        to_make_transparent = []

        # 从四条边缘开始
        edge_pixels = []
        for x in range(width):
            edge_pixels.append((x, 0))           # 顶边
            edge_pixels.append((x, height - 1))  # 底边
        for y in range(height):
            edge_pixels.append((0, y))           # 左边
            edge_pixels.append((width - 1, y))   # 右边

        queue = []
        for x, y in edge_pixels:
            if not visited[y][x]:
                pixel_color = pixels[x, y][:3]
                if colors_match(pixel_color, bg_color, tolerance):
                    queue.append((x, y))
                    visited[y][x] = True

        # BFS洪水填充
        while queue:
            x, y = queue.pop(0)
            to_make_transparent.append((x, y))

            # 检查4个相邻像素
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                    pixel_color = pixels[nx, ny][:3]
                    if colors_match(pixel_color, bg_color, tolerance):
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        # 将所有标记的像素设为透明
        for x, y in to_make_transparent:
            pixels[x, y] = (0, 0, 0, 0)

        return result


    def export_data_file(
        self,
        output_path: str,
        format: str = "json"
    ) -> str:
        """
        导出精灵数据文件

        Args:
            output_path: 输出路径
            format: 格式 (json, 后续可支持xml等)

        Returns:
            保存的文件路径
        """
        if not self.sprites:
            raise ValueError("请先执行拆分操作")

        print(f"\n📝 导出数据文件:")
        print(f"  输出路径: {output_path}")

        if format == "json":
            data = {
                "image": os.path.basename(self.image_path),
                "size": {
                    "width": self.image.width,
                    "height": self.image.height
                },
                "sprites": [
                    {
                        "name": sprite.name,
                        "x": sprite.x,
                        "y": sprite.y,
                        "width": sprite.width,
                        "height": sprite.height
                    }
                    for sprite in self.sprites
                ]
            }

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"  ✓ 已导出数据文件")
        return output_path

    def preview_sprites(self, output_path: str = None) -> Image.Image:
        """
        生成预览图（在原图上标记精灵区域）

        Args:
            output_path: 可选，保存预览图的路径

        Returns:
            预览图Image对象
        """
        if not self.image:
            raise ValueError(i18n.t("err_no_image"))

        if not self.sprites:
            raise ValueError(i18n.t("err_no_sprites"))

        from PIL import ImageDraw, ImageFont

        # 复制原图
        preview = self.image.copy()
        draw = ImageDraw.Draw(preview)

        # 颜色列表，用于区分不同的精灵
        colors = [
            (255, 0, 0, 200),    # 红
            (0, 255, 0, 200),    # 绿
            (0, 0, 255, 200),    # 蓝
            (255, 255, 0, 200),  # 黄
            (255, 0, 255, 200),  # 紫
            (0, 255, 255, 200),  # 青
        ]

        for i, sprite in enumerate(self.sprites):
            color = colors[i % len(colors)]

            # 画矩形边框
            draw.rectangle(
                [sprite.x, sprite.y, sprite.x + sprite.width - 1, sprite.y + sprite.height - 1],
                outline=color[:3],
                width=2
            )

            # 标注索引
            draw.text((sprite.x + 2, sprite.y + 2), str(i), fill=color[:3])

        if output_path:
            preview.save(output_path)
            print(f"✓ 预览图已保存: {output_path}")

        return preview


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='精灵表拆分器 - 模仿TexturePacker的简易版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # Grid模式 - 按精灵尺寸拆分
  python sprite_splitter.py image.png -m grid -sw 64 -sh 64 -o output/

  # Grid模式 - 按行列数拆分
  python sprite_splitter.py image.png -m grid -c 4 -r 4 -o output/

  # Rectangular模式 - 自动检测
  python sprite_splitter.py image.png -m rect -o output/

  # Data File模式 - 使用JSON文件
  python sprite_splitter.py image.png -m data -d sprites.json -o output/
        '''
    )

    parser.add_argument('image', nargs='?', help='精灵表图片路径 (data模式可省略)')
    parser.add_argument('-m', '--mode', choices=['grid', 'rect', 'data'], default='grid',
                        help='拆分模式: grid(网格), rect(矩形检测), data(数据文件)')
    parser.add_argument('-o', '--output', default='./output', help='输出目录')
    parser.add_argument('-f', '--format', default='png', help='输出格式 (png, jpg, webp)')
    parser.add_argument('-t', '--template', default='{name}', help='命名模板')
    parser.add_argument('--trim', action='store_true', help='裁剪透明边缘')
    parser.add_argument('--preview', action='store_true', help='生成预览图')

    # Grid模式参数
    parser.add_argument('-c', '--columns', type=int, default=0, help='Grid模式: 列数')
    parser.add_argument('-r', '--rows', type=int, default=0, help='Grid模式: 行数')
    parser.add_argument('-sw', '--sprite-width', type=int, default=0, help='Grid模式: 精灵宽度')
    parser.add_argument('-sh', '--sprite-height', type=int, default=0, help='Grid模式: 精灵高度')
    parser.add_argument('-p', '--padding', type=int, default=0, help='Grid模式: 精灵间距')
    parser.add_argument('--margin', type=int, default=0, help='Grid模式: 边缘间距')

    # Rectangular模式参数
    parser.add_argument('--min-width', type=int, default=1, help='Rect模式: 最小宽度')
    parser.add_argument('--min-height', type=int, default=1, help='Rect模式: 最小高度')
    parser.add_argument('--alpha-threshold', type=int, default=0, help='Rect模式: Alpha阈值')

    # Data File模式参数
    parser.add_argument('-d', '--data-file', help='Data模式: JSON数据文件路径')
    parser.add_argument('--restore-source', action='store_true', help='还原原始尺寸 (offX/offY/sourceW/sourceH)')
    parser.add_argument('--offset-origin', choices=['top', 'bottom'], default='top', help='偏移原点: top(左上), bottom(左下)')

    args = parser.parse_args()

    try:
        image_path = args.image
        if args.mode == 'data':
            if not args.data_file:
                print("错误: Data模式需要指定 -d/--data-file 参数")
                return 1
            if not image_path:
                image_path = resolve_image_path_from_data_file(args.data_file)
                if not image_path:
                    print("错误: Data模式需要图片路径或JSON包含file/meta.image")
                    return 1

        if not image_path:
            print("错误: 请指定图片路径")
            return 1

        # 创建拆分器
        splitter = SpriteSplitter(image_path)
        splitter.offset_origin = args.offset_origin

        # 执行拆分
        if args.mode == 'grid':
            splitter.split_by_grid(
                columns=args.columns,
                rows=args.rows,
                sprite_width=args.sprite_width,
                sprite_height=args.sprite_height,
                padding=args.padding,
                margin=args.margin
            )
        elif args.mode == 'rect':
            splitter.split_by_rectangle(
                min_width=args.min_width,
                min_height=args.min_height,
                alpha_threshold=args.alpha_threshold
            )
        elif args.mode == 'data':
            splitter.split_by_data_file(args.data_file)
            if args.restore_source:
                splitter.restore_source = True

        # 生成预览
        if args.preview:
            preview_path = os.path.join(args.output, '_preview.png')
            os.makedirs(args.output, exist_ok=True)
            splitter.preview_sprites(preview_path)

        # 保存精灵
        splitter.save_sprites(
            output_dir=args.output,
            name_template=args.template,
            format=args.format,
            trim=args.trim
        )

        # 导出数据文件
        data_path = os.path.join(args.output, '_sprites.json')
        splitter.export_data_file(data_path)

        print("\n✅ 拆分完成!")
        return 0

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
