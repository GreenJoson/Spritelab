# SpriteLab · Sprite Sheet Splitter

[English](README.md) | [简体中文](#简体中文)

[![GitHub](https://img.shields.io/badge/GitHub-SpriteLab-181717?logo=github)](https://github.com/GreenJoson/Spritelab)
[![Official Site](https://img.shields.io/badge/Official-spritelab.app-blue)](https://spritelab.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SpriteLab Splitter is a high-performance desktop utility for game developers to unpack sprite sheets into individual frames. This is a standalone tool that works offline.

Official Website: **[spritelab.app](https://spritelab.app)**

---

## English

A powerful desktop tool to split sprite sheets (Texture Atlases) using multiple intelligent modes. Built for precision and ease of use.

### Key Features
- **Grid Mode**: Split by fixed columns/rows or pixel dimensions.
- **Rectangular Mode**: Smart boundary detection using alpha transparency or background color.
- **Data File Mode**: Import and split via JSON data files (TexturePacker format), supports offX/offY/sourceW/sourceH restore and JSON-based image auto-resolve.
- **Internationalization**: Full support for English and Chinese.
- **Real-time Preview**: Precise visual feedback before exporting.
- **Batch Processing**: Smart edge trimming, background removal, and asset renaming.

### Downloads
- **Latest Version**: Download from [GitHub Releases](https://github.com/GreenJoson/Spritelab/releases)
- **CI Builds**: Get development builds from GitHub Actions (Signed-in users).

### Tech Stack
- **Language**: Python 3.13
- **GUI**: Tkinter
- **Image Processing**: Pillow
- **Packaging**: PyInstaller

### Local Setup
```bash
# Clone the repository
git clone https://github.com/GreenJoson/Spritelab.git
cd Spritelab

# Install dependencies
pip install -r requirements.txt

# Run the app
python gui.py
```

---

## 简体中文

SpriteLab Splitter 是一款高性能的桌面端工具，专门为游戏开发者设计，用于将精灵表（Sprite Sheets）拆分为独立的帧。这是一款完全支持离线使用的独立工具。

官方网站：**[spritelab.app](https://spritelab.app)**

### 核心功能
- **网格模式**: 按固定的行列或像素尺寸进行拆分。
- **矩形模式**: 通过透明度或背景色智能识别精灵边界。
- **数据文件模式**: 支持导入 JSON 数据文件（如 TexturePacker 格式）进行拆分，支持 offX/offY/sourceW/sourceH 还原原始尺寸，并可自动解析 JSON 中的图片路径。
- **多语言支持**: 完美支持中文和英文。
- **实时预览**: 导出前提供精确的视觉反馈。
- **批量处理**: 支持智能边缘裁剪、去背景和资产重命名。

### 下载地址
- **最新版本**: 从 [GitHub Releases](https://github.com/GreenJoson/Spritelab/releases) 下载。
- **开发构件**: 登录后可从 GitHub Actions 下载最新的自动化构件。

### 技术栈
- **编程语言**: Python 3.13
- **图形界面**: Tkinter
- **图像处理**: Pillow
- **应用打包**: PyInstaller

### 本地运行
```bash
# 克隆仓库
git clone https://github.com/GreenJoson/Spritelab.git
cd Spritelab

# 安装依赖
pip install -r requirements.txt

# 运行程序
python gui.py
```

### 开源协议
MIT
