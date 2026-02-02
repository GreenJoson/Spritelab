---
name: spritelab-release-ops
description: SpriteLab（桌面端）发布与官网同步的默认工作流（Codex/Agent 执行约束）
---

# SpriteLab 发布与官网同步约束（必须执行）

> ⚠️ 本仓库任何功能/修复一旦合入，**不要停在“代码改完”**：必须完成“发布 + 本机替换 + 官网同步 + 部署”闭环。

## 0. 关键事实（避免踩坑）

- GitHub Actions 打包工作流（`.github/workflows/build.yml`）**只会在 push tag `v*` 时触发**，不是 push `main`。
- macOS 图标必须通过 PyInstaller `--icon icon.icns`，否则会出现 Python 默认图标。
- Windows 图标必须准备 `icon.ico` 并在 PyInstaller 里 `--icon icon.ico`。

## 1. 每次改动后的“发布闭环”（默认必须做）

### 1.1 自测（本地）

- 运行：`python3 -m unittest`

### 1.2 版本号（必须）

- 更新 `version_checker.py` 的 `CURRENT_VERSION`（例如 `v1.0.18` → `v1.0.19`）
- 同步更新 `i18n.py` 中显示版本号（中英 title / hint）

### 1.3 提交与推送（必须）

- `git status` 确认无多余文件（尤其是本地工具生成目录）
- `git add ... && git commit -m "fix|feat|chore: ..."`
- `git push origin main`

### 1.4 打 tag 触发自动打包与 Release（必须）

- `git tag -a vX.Y.Z -m "vX.Y.Z"`
- `git push origin vX.Y.Z`
- 用 `gh run list` / `gh run watch` 等待 `Build SpriteLab` 完成
- 用 `gh release view vX.Y.Z` 确认生成了：
  - `SpriteLab-macOS.zip`
  - `SpriteLab-Windows.zip`

### 1.5 自动替换本机 macOS App（必须）

- **优先本地打包产物覆盖**：如果你本地已经完成 PyInstaller 打包（`dist/SpriteLab.app` 已生成），直接用它覆盖 `/Applications/SpriteLab.app`，不需要再从 GitHub 下载再覆盖（除非你需要 CI 产物/签名产物）。
- 下载并覆盖安装到 `/Applications/SpriteLab.app`：
  - `gh release download vX.Y.Z -p SpriteLab-macOS.zip`
  - `unzip SpriteLab-macOS.zip`
  - 用 `ditto` 复制 `SpriteLab.app` 覆盖 `/Applications/SpriteLab.app`
- 清除隔离属性（避免 Gatekeeper 弹窗）：`xattr -dr com.apple.quarantine /Applications/SpriteLab.app`
- 让 Finder/Dock 刷新图标缓存（必要时）：`touch /Applications/SpriteLab.app && killall Finder`

## 2. 官网同步（必须一起做）

> 目标仓库：`~/Projects/Nodejs/tools/SpriteLab`

### 2.1 更新最新版本与更新日志

- 更新下载页的版本号、发布日期、更新日志（changelog / release notes）
- 更新下载链接指向最新 GitHub Release（推荐使用 `releases/latest` 或最新 tag）

### 2.2 触发部署（必须）

- 在官网仓库提交并 `git push`，确保 GitHub Actions 部署触发并成功。

## 3. 图标与打包约束（禁止回退）

- `.github/workflows/build.yml` 的 PyInstaller 命令必须包含：
  - macOS：`--icon icon.icns`
  - Windows：`--icon icon.ico`
- `icon.icns` / `icon.ico` 必须存在且随仓库管理。
