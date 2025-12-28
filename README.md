# 精灵表拆分器 (Sprite Sheet Splitter)

一个使用 Python 实现的精灵表拆分工具，模仿 TexturePacker 的功能设计。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pillow](https://img.shields.io/badge/Pillow-9.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 功能特性

### 三种拆分模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **Grid** | 按固定网格拆分 | 所有精灵大小一致、规则排列 |
| **Rectangular** | 自动检测透明边界分隔的矩形区域 | 精灵大小不一、有透明分隔 |
| **Data File** | 使用 JSON 数据文件精确拆分 | 有现成的精灵表数据 |

### 其他功能

- ✅ 命令行工具 (CLI)
- ✅ 图形界面 (GUI)
- ✅ 实时预览
- ✅ 自定义命名模板
- ✅ 多种输出格式 (PNG, JPG, WebP)
- ✅ 裁剪透明边缘
- ✅ 导出精灵数据文件
- ✅ 预览图生成

### GUI预览功能（模仿TexturePacker）

| 功能 | 描述 |
|------|------|
| **蓝色边框** | 精灵表外围显示蓝色边框，标识图片范围 |
| **白色网格线** | 拆分后显示白色网格线，标识每个精灵的边界 |
| **实时预览** | 修改Grid参数（列数/行数等）时自动更新网格预览，无需点击拆分 |
| **选中高亮** | 点击精灵时显示绿色边框高亮，支持在预览或列表中选择 |
| **居中显示** | 图片始终保持在预览区域居中 |
| **缩放控制** | 支持滚轮缩放、适应窗口、1:1显示 |

## 安装

### 依赖

```bash
pip install Pillow
```

### 可选依赖（拖放支持）

```bash
pip install tkinterdnd2
```

## 使用方法

### 命令行工具

#### Grid 模式 - 按精灵尺寸拆分

```bash
python sprite_splitter.py image.png -m grid -sw 64 -sh 64 -o output/
```

#### Grid 模式 - 按行列数拆分

```bash
python sprite_splitter.py image.png -m grid -c 4 -r 4 -o output/
```

#### Rectangular 模式 - 自动检测

```bash
python sprite_splitter.py image.png -m rect -o output/
```

#### Data File 模式 - 使用 JSON 文件

```bash
python sprite_splitter.py image.png -m data -d sprites.json -o output/
```

### 命令行参数详解

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `image` | 精灵表图片路径 | 必填 |
| `-m, --mode` | 拆分模式 (grid/rect/data) | grid |
| `-o, --output` | 输出目录 | ./output |
| `-f, --format` | 输出格式 (png/jpg/webp) | png |
| `-t, --template` | 命名模板 | {name} |
| `--trim` | 裁剪透明边缘 | False |
| `--preview` | 生成预览图 | False |

#### Grid 模式参数

| 参数 | 说明 |
|------|------|
| `-c, --columns` | 列数 |
| `-r, --rows` | 行数 |
| `-sw, --sprite-width` | 精灵宽度 |
| `-sh, --sprite-height` | 精灵高度 |
| `-p, --padding` | 精灵间距 |
| `--margin` | 边缘间距 |

#### Rectangular 模式参数

| 参数 | 说明 |
|------|------|
| `--min-width` | 最小精灵宽度 |
| `--min-height` | 最小精灵高度 |
| `--alpha-threshold` | Alpha 阈值 (0-255) |

#### Data File 模式参数

| 参数 | 说明 |
|------|------|
| `-d, --data-file` | JSON 数据文件路径 |

### 图形界面

```bash
python gui.py
```

## 命名模板

命名模板支持以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{name}` | 精灵名称 | sprite_0001 |
| `{index}` | 精灵索引 | 0, 1, 2... |
| `{x}` | X 坐标 | 64 |
| `{y}` | Y 坐标 | 128 |
| `{width}` | 精灵宽度 | 32 |
| `{height}` | 精灵高度 | 32 |

### 示例

```bash
# 输出 frame_0.png, frame_1.png, ...
python sprite_splitter.py image.png -m grid -c 4 -r 4 -t "frame_{index}"

# 输出 sprite_64_128.png (按坐标命名)
python sprite_splitter.py image.png -m rect -t "sprite_{x}_{y}"
```

## JSON 数据文件格式

### TexturePacker Hash 格式

```json
{
  "frames": {
    "sprite_001.png": {
      "frame": {"x": 0, "y": 0, "w": 64, "h": 64}
    },
    "sprite_002.png": {
      "frame": {"x": 64, "y": 0, "w": 64, "h": 64}
    }
  }
}
```

### TexturePacker Array 格式

```json
{
  "frames": [
    {
      "filename": "sprite_001.png",
      "frame": {"x": 0, "y": 0, "w": 64, "h": 64}
    }
  ]
}
```

### 简单格式

```json
{
  "sprites": [
    {"name": "sprite_001", "x": 0, "y": 0, "width": 64, "height": 64}
  ]
}
```

## API 使用

```python
from sprite_splitter import SpriteSplitter

# 创建拆分器
splitter = SpriteSplitter("spritesheet.png")

# Grid 模式拆分
sprites = splitter.split_by_grid(columns=4, rows=4)

# 或使用精灵尺寸
sprites = splitter.split_by_grid(sprite_width=64, sprite_height=64)

# Rectangular 模式拆分
sprites = splitter.split_by_rectangle(min_width=10, min_height=10)

# Data File 模式拆分
sprites = splitter.split_by_data_file("sprites.json")

# 保存精灵
saved_files = splitter.save_sprites(
    output_dir="output",
    name_template="{name}",
    format="png",
    trim=True
)

# 导出数据文件
splitter.export_data_file("sprites_data.json")

# 生成预览图
preview = splitter.preview_sprites("preview.png")
```

## 项目结构

```
sprite_sheet_splitter/
├── sprite_splitter.py   # 核心拆分器模块
├── gui.py               # 图形界面
├── README.md            # 项目文档
└── requirements.txt     # 依赖列表
```

## 与 TexturePacker 功能对比

| 功能 | TexturePacker | 本工具 |
|------|---------------|--------|
| Grid 模式 | ✅ | ✅ |
| Rectangular 模式 | ✅ | ✅ |
| Data File 模式 | ✅ | ✅ |
| 自定义命名 | ✅ | ✅ |
| 裁剪透明边缘 | ✅ | ✅ |
| 预览功能 | ✅ | ✅ |
| 多格式输出 | ✅ | ✅ |
| 旋转恢复 | ✅ | ❌ |
| 商业授权 | 需购买 | 免费开源 |

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-12-27)

- 初始版本
- 支持 Grid、Rectangular、Data File 三种拆分模式
- 命令行工具和图形界面
- 自定义命名模板
- 多格式输出支持
