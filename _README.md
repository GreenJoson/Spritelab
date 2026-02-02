# sprite_sheet_splitter - 精灵表拆分工具

> ⚠️ 一旦本文件夹有所变化，请更新本文件

| 文件名 | 地位 | 功能 |
|---|---|---|
| sprite_splitter.py | 核心 | 拆分逻辑与Data File解析/还原 |
| gui.py | 核心 | Tkinter 图形界面与交互（输出设置布局/数据文件刷新） |
| i18n.py | 基础 | 多语言文案管理 |
| README.md | 文档 | 使用说明与功能概览 |
| AGENTS.md / AGENT.md | 规范 | Agent 执行约束（发布闭环 + 官网同步） |
| icon.icns / icon.ico | 资源 | 应用图标（macOS/Windows 打包） |
| tests/test_restore_mode.py | 测试 | Data File 还原尺寸回归测试 |
| tests/test_name_template.py | 测试 | 空模板命名回退测试 |
| tests/test_res_mc_format.py | 测试 | res/mc JSON 解析测试 |
| tests/test_fit_padding.py | 测试 | fit 等比缩放导出透明补边回归测试 |
