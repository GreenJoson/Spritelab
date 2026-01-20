# 精灵表还原尺寸设计

## 目标
- 支持从 JSON（含 offX/offY/sourceW/sourceH 或 TexturePacker 格式）还原原始尺寸。
- JSON 内含图片路径时可自动解析并加载。
- 保持现有 Grid/Rect 模式行为不变。

## 约束
- 不引入付费工具（TexturePacker）。
- 兼容现有 Data File JSON 与 TexturePacker JSON。
- 默认保持透明背景。

## 方案对比
1. **自动还原（推荐）**
   - Data File 中存在 source 尺寸时自动还原，无需用户额外操作。
   - 优点：最少操作、符合需求。
   - 缺点：如果用户希望保持裁剪结果，需要手动关闭。

2. **显式开关**
   - 通过 GUI/CLI 勾选是否还原。
   - 优点：可控性更强。
   - 缺点：多一步操作。

## 选定方案
- Data File 有 source 尺寸时默认开启还原，GUI 提供“还原原始尺寸”开关，允许关闭。
- 增加“偏移原点（左上/左下）”以兼容不同 JSON 坐标系。

## 数据流
- 读取 JSON → 解析 frame 与 offX/offY/sourceW/sourceH → 生成 SpriteRect。
- 保存时裁剪 frame → 按 offset 贴到 source 尺寸透明画布 → 输出。

## 错误处理
- JSON 中无图片路径则不自动加载。
- source 尺寸缺失时自动回退为普通裁剪。

## 测试
- 新增单元测试，校验输出尺寸与 sourceW/sourceH 一致。

## UI 变更
- 输出设置新增“还原原始尺寸”与“偏移原点”选项。
