# SpriteLab · AI Game Asset Generator & Sprite Splitter

[English](README.md) | [简体中文](#简体中文)

[![GitHub](https://img.shields.io/badge/GitHub-SpriteLab-181717?logo=github)](https://github.com/GreenJoson/Spritelab)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SpriteLab is a powerful suite for game developers to create and manage game assets. It features an AI-powered asset generator and a high-performance sprite sheet splitter.

---

## English

SpriteLab turns prompts into game-ready art (backgrounds, characters, UI, icons, sprite animations) via Google Gemini 2.0 Images (through ZenMux).

### Main Components
- **SpriteLab Web**: AI Generation platform (FastAPI + Celery + Redis + React).
- **SpriteLab Tool**: Desktop Sprite Sheet Splitter (Python + Tkinter) for offline asset processing.

### Repo & Downloads
- **Code**: [GitHub Repository](https://github.com/GreenJoson/Spritelab)
- **CI Builds**: GitHub Actions → **Build SpriteLab** workflow → artifacts (SpriteLab-Windows / SpriteLab-macOS).
  *Note: Signed-in GitHub users can access artifacts. For public releases, check the [Releases](https://github.com/GreenJoson/Spritelab/releases) page.*

### Project Structure (Monorepo)
```
SpriteLab/
├── apps/
│   ├── web/          # Frontend (React + Vite + shadcn/ui) [WIP]
│   └── api/          # Backend (Python + FastAPI) ✅
├── packages/
│   └── shared/       # Shared types ✅
└── docs/             # Documentation
```

### Features
- **Asset Generation**: Backgrounds, characters/NPCs, UI buttons, icons, animations, 9-slice borders, items.
- **Customization**: Portrait/Landscape/Square orientations; Pixel art, hand-drawn, realistic, cartoon, low poly, isometric styles.
- **Sprite Splitter**:
  - **Grid Mode**: Split by fixed grid.
  - **Rectangular Mode**: Smart detection of sprite boundaries via transparency.
  - **Data File Mode**: Support for TexturePacker JSON export.

### Quickstart (Local Development)
#### One-liner
```bash
./start.sh
```
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:3000/docs

#### Manual Setup
```bash
# Install dependencies
pnpm install
cd apps/api && pip install -r requirements.txt

# Configure Environment (apps/api/.env)
ZENMUX_API_KEY=sk-ai-v1-your-key-here
ZENMUX_BASE_URL=https://zenmux.ai/api/vertex-ai
REDIS_URL=redis://localhost:6379
```

### Tech Stack
- **Backend**: FastAPI, Google Generative AI (Gemini via ZenMux), Celery + Redis, Pillow.
- **Frontend**: React 18, Vite, shadcn/ui, TailwindCSS, Pixi.js, Zustand.
- **Desktop**: Python 3.13, Tkinter, PyInstaller.

### Roadmap
- **Frontend**: Pixi.js preview/editing, sprite sheet packer, animation frames.
- **Backend**: Multi-engine export (Godot/Unity/Cocos), WebSocket realtime updates.
- **Production**: Docker Compose, Nginx setup.

### Contributing
PRs and issues are welcome! Please follow [Conventional Commits](https://www.conventionalcommits.org/).

### License
MIT

---

## 简体中文

SpriteLab 是一个为游戏开发者打造的强大工具集，涵盖了 AI 素材生成和高性能精灵表（Sprite Sheet）切割功能。

### 主要组件
- **SpriteLab Web**: AI 生成平台（基于 FastAPI + Celery + Redis + React）。
- **SpriteLab Tool**: 桌面端精灵表拆分器（基于 Python + Tkinter），用于离线素材处理。

### 仓库与下载
- **代码库**: [GitHub Repository](https://github.com/GreenJoson/Spritelab)
- **持续集成**: GitHub Actions → **Build SpriteLab** 工作流 → 产物 (SpriteLab-Windows / SpriteLab-macOS)。
  *注意：登录 GitHub 后即可在 Actions 页面下载产物。公共下载请关注 [Releases](https://github.com/GreenJoson/Spritelab/releases) 页面。*

### 项目结构
```
SpriteLab/
├── apps/
│   ├── web/          # 前端 (React + Vite + shadcn/ui) [开发中]
│   └── api/          # 后端 (Python + FastAPI) ✅
├── packages/
│   └── shared/       # 共享类型定义 ✅
└── docs/             # 项目文档
```

### 功能特性
- **素材生成**: 背景、角色/NPC、UI 按钮、图标、动画帧、九宫格边框、道具。
- **自定义选项**: 支持横屏/竖屏/正方形；提供像素风、手绘、写实、卡通、低多边形、等距视角等多种风格。
- **精灵表拆分**:
  - **网格模式**: 按固定行列拆分。
  - **矩形模式**: 通过透明度自动识别精灵边界。
  - **数据文件模式**: 支持 TexturePacker JSON 格式。

### 快速开始 (本地开发)
#### 一键启动
```bash
./start.sh
```
- **前端地址**: http://localhost:5173
- **API 文档**: http://localhost:3000/docs

### 技术栈
- **后端**: FastAPI, Google Gemini (通过 ZenMux), Celery + Redis, Pillow.
- **前端**: React 18, Vite, shadcn/ui, TailwindCSS, Pixi.js, Zustand.
- **桌面端**: Python 3.13, Tkinter, PyInstaller.

### 路线图
- **前端增强**: Pixi.js 预览编辑、精灵表打包、动画帧预览。
- **后端增强**: 多引擎导出支持 (Godot/Unity/Cocos), WebSocket 实时更新。
- **部署**: Docker Compose 支持, Nginx 配置优化。

### 参与贡献
欢迎提交 PR 或 Issue！请遵循 [约定式提交 (Conventional Commits)](https://www.conventionalcommits.org/zh-hans/) 规范。

### 开源协议
MIT
