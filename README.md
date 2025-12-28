# 🎮 SpriteLab - 精灵表拆分器

[![Build SpriteLab](https://github.com/GreenJoson/Spritelab/actions/workflows/build.yml/badge.svg)](https://github.com/GreenJoson/Spritelab/actions/workflows/build.yml)

**官网: [SpriteLab.app](https://spritelab.app)**

一个功能强大的精灵表/精灵图拆分工具，支持多种拆分模式和智能检测。

![SpriteLab Screenshot](icon.png)

## ✨ 功能特性

### 拆分模式
- **Grid模式** - 按行列数均匀拆分
- **Rectangular模式** - 自动识别精灵边界（支持透明背景和纯色背景）
- **Data File模式** - 使用JSON数据文件拆分

### 智能功能
- 🔍 **智能背景检测** - 自动识别透明或纯色背景
- ✂️ **边缘裁剪** - 去除精灵边缘分隔线
- 🎨 **智能去背景** - 从边缘去除纯色背景，保留内部
- 📐 **批量调整大小** - 按比例或自定义尺寸批量缩放

### 其他特性
- 🌐 多语言支持（中文/English）
- 💾 导出JSON数据文件
- 🖼️ 实时预览
- 🗑️ 精灵管理（删除、重新编号）

## 📥 下载

### macOS
从 [Releases](https://github.com/GreenJoson/Spritelab/releases) 下载 `SpriteLab-macOS.zip`

### Windows
从 [Releases](https://github.com/GreenJoson/Spritelab/releases) 下载 `SpriteLab-Windows.zip`

## 🛠️ 从源码运行

### 依赖安装
```bash
pip install -r requirements.txt
```

### 运行
```bash
python gui.py
```

## 📦 打包

### macOS
```bash
pyinstaller --windowed --name "SpriteLab" --icon icon.icns --add-data "sprite_splitter.py:." --add-data "i18n.py:." gui.py
```

### Windows
双击运行 `build_windows.bat` 或：
```cmd
pyinstaller --windowed --name "SpriteLab" --add-data "sprite_splitter.py;." --add-data "i18n.py;." gui.py
```

## 📝 使用说明

1. **打开图片** - 点击"打开图片"按钮或拖放图片
2. **选择模式** - Grid/Rectangular/数据文件
3. **配置参数** - 设置行列数或最小尺寸
4. **执行拆分** - 点击"执行拆分"
5. **保存精灵** - 选择输出目录，点击"保存精灵"

## 📄 License

MIT License

---

**SpriteLab.app** - 让精灵拆分变得简单！
