#!/usr/bin/env python3
"""
@input  依赖：LANGUAGES 字典
@output 导出：i18n 文案查找
@pos    全局文案与多语言入口

⚠️ 一旦本文件被更新，务必更新以上注释

多语言支持模块
支持中文和英文
"""

# 语言字典
LANGUAGES = {
    "zh": {
        # 窗口标题
        "app_title": "SpriteLab v1.0.11 - 精灵表拆分器 | SpriteLab.app",

        # 菜单
        "menu_file": "文件",
        "menu_open": "打开图片",
        "menu_save": "保存精灵",
        "menu_export": "导出数据文件",
        "menu_exit": "退出",
        "menu_edit": "编辑",
        "menu_view": "视图",
        "menu_zoom_in": "放大",
        "menu_zoom_out": "缩小",
        "menu_clear": "清除",
        "menu_help": "帮助",
        "menu_usage": "使用说明",
        "menu_about": "关于",
        "menu_language": "语言",

        # 工具栏
        "toolbar_open": "打开图片",
        "toolbar_save": "保存精灵",
        "toolbar_split": "执行拆分",
        "toolbar_clear": "清除",
        "toolbar_zoom": "缩放:",
        "toolbar_fit": "适合",

        # 面板
        "panel_sprite_list": "精灵列表",
        "panel_preview": "预览",
        "panel_settings": "设置",

        # 精灵列表
        "sprite_count": "共 {count} 个精灵",
        "sprite_preview_count": "预览: {count} 个精灵",
        "btn_delete": "🗑 删除",
        "btn_renumber": "🔢 重新编号",

        # 设置面板
        "splitter_title": "精灵表拆分器",
        "split_mode": "拆分模式",
        "mode_grid": "Grid",
        "mode_rect": "Rectangular",
        "mode_data": "数据文件",

        # Grid设置
        "grid_settings": "Grid设置",
        "grid_columns": "Columns:",
        "grid_rows": "Rows:",
        "sprite_width": "精灵宽度:",
        "sprite_height": "精灵高度:",
        "padding": "形状填充:",
        "margin": "边框填充:",

        # Rectangular设置
        "rect_settings": "Rectangular设置",
        "min_width": "最小宽度:",
        "min_height": "最小高度:",
        "alpha_threshold": "Alpha阈值:",

        # 数据文件设置
        "data_settings": "数据文件设置",
        "data_file": "数据文件:",
        "browse": "浏览",

        # 输出设置
        "output_settings": "输出设置",
        "output_dir": "输出目录:",
        "name_template": "精灵名称模板:",
        "template_help": "可用: {name} {index} {x} {y} {width} {height}  例: light_{index}",
        "format": "格式:",
        "trim_transparent": "裁剪透明边缘",
        "restore_source": "还原原始尺寸",
        "offset_origin": "偏移原点",
        "offset_origin_top": "左上",
        "offset_origin_bottom": "左下",
        "edge_crop": "边缘裁剪:",
        "edge_crop_hint": "(去除边缘分隔线)",
        "smart_edge": "智能边缘检测",
        "smart_edge_hint": "(自动移除白色分隔线)",
        "remove_bg": "智能去背景",
        "remove_bg_hint": "(去除边缘纯色背景，保留内部)",
        "btn_apply": "应用",
        "btn_save_sprites": "💾 保存精灵",

        # 批量调整大小
        "resize_settings": "批量调整大小",
        "resize_mode": "缩放模式:",
        "resize_none": "不缩放",
        "resize_scale": "按比例",
        "resize_custom": "自定义尺寸",
        "scale_ratio": "缩放比例:",
        "target_width": "宽度:",
        "target_height": "高度:",
        "keep_ratio": "保持宽高比",

        # 状态栏
        "status_ready": "就绪",
        "status_loaded": "已加载: {filename}",
        "status_split_done": "拆分完成，共 {count} 个精灵",
        "status_saved": "已保存 {count} 个精灵到 {path}",
        "status_loaded": "已加载: {name}",
        "status_clipboard_loaded": "已从剪贴板加载: {name}",
        "status_split_complete": "拆分完成，共 {count} 个精灵",
        "status_saved_to": "已保存 {count} 个精灵到 {path}",
        "status_deleted": "已删除精灵，剩余 {count} 个",
        "status_deleted_all": "已删除全部精灵",
        "status_renumbered": "已重新编号 {count} 个精灵",
        "status_exported": "数据文件已导出: {path}",
        "status_selected": "选中: {name} - 位置({x}, {y}) 尺寸({w}x{h})",
        "sprite_count_total": "共 {count} 个精灵",
        "sprite_count_preview": "预览: {count} 个精灵",
        "size_info": "{w} x {h}, {count} 个精灵",

        # 对话框
        "warning": "警告",
        "error": "错误",
        "success": "成功",
        "confirm": "确认",
        "info": "提示",

        # 消息标题
        "title_warning": "警告",
        "title_info": "提示",
        "title_error": "错误",
        "title_success": "成功",
        "title_confirm": "确认",
        "title_complete": "完成",

        # 详细消息
        "msg_clipboard_not_image": "剪贴板中的文件不是支持的图片格式",
        "msg_clipboard_help": "请复制图片文件的完整路径，或直接使用'打开图片'按钮",
        "msg_clipboard_empty": "剪贴板为空或不包含文件路径\n\n请复制图片文件的完整路径",
        "msg_paste_failed": "粘贴失败: {error}",
        "msg_load_failed": "加载图片失败: {error}",
        "msg_split_failed": "拆分失败: {error}",
        "msg_save_failed": "保存失败: {error}",
        "msg_export_failed": "导出失败: {error}",
        "msg_template_applied": "已应用名称模板到 {count} 个精灵",
        "msg_select_data_first": "请选择数据文件",

        # 消息
        "msg_load_image": "请先加载图片",
        "msg_do_split": "请先执行拆分操作",
        "err_no_image": "请加载图片",
        "err_no_sprites": "请先执行拆分",
        "msg_select_sprite": "请先选中要删除的精灵",
        "msg_no_sprites": "没有精灵需要编号",
        "msg_delete_all": "确定要删除全部精灵吗？",
        "msg_save_success": "已保存 {count} 个精灵到:\n{path}",
        "msg_select_data": "请选择数据文件",

        # 帮助
        "help_title": "使用说明",
        "about_title": "关于",
        "opensource_hint": "免费版 v1.0.11 | SpriteLab.app",

        # 预览提示
        "preview_hint": "双击此处打开图片\n或使用 Cmd+V 粘贴图片路径\n或点击'打开图片'按钮",

        # 右键菜单
        "ctx_delete": "删除选中精灵",
        "ctx_renumber": "重新编号",
        "ctx_delete_all": "全部删除",

        # 帮助长文本
        "help_text": """
精灵表拆分器使用说明:

1. 打开精灵表图片
   - 拖拽图片到窗口
   - 使用 Cmd+V 粘贴图片文件路径
   - 使用 Cmd+O 快捷键打开

2. 选择拆分模式
   - Grid: 按固定网格拆分，适合规则排列的精灵
   - Rectangular: 自动检测透明边界分隔的区域
   - 数据文件: 使用JSON数据文件拆分

3. 配置拆分参数
   - Grid模式: 设置列数/行数或精灵尺寸
   - Rectangular模式: 设置最小尺寸和Alpha阈值
   - 数据文件模式: 选择JSON文件

4. 执行拆分
   - 点击工具栏的"执行拆分"按钮(放大镜图标)
   - 检查预览区域是否正确识别了精灵

5. 保存精灵
   - 点击"保存精灵"按钮
   - 配置输出目录和命名模板

命名模板支持的变量:
{name} - 原文件名
{index} - 精灵索引
{x}, {y} - 位置坐标
{width}, {height} - 尺寸
""",
        "about_text": """
精灵表拆分器 (Sprite Sheet Splitter)

版本: {version}
作者: AI Assistant

这是一个模仿TexturePacker功能的简易版本，
使用Python + Pillow + tkinter实现。

功能特性:
- Grid模式网格拆分
- Rectangular模式自动检测
- Data File模式数据文件拆分
- 实时预览和缩放
- 选中精灵高亮显示
- 自定义输出设置
- 多语言支持

开源免费，欢迎使用和贡献！
""",

        # 更新
        "update_available": "发现新版本: {version}",
        "btn_update": "⬇️ 更新",
    },

    "en": {
        # Window title
        "app_title": "SpriteLab v1.0.11 - Sprite Sheet Splitter | SpriteLab.app",

        # Menu
        "menu_file": "File",
        "menu_open": "Open Image",
        "menu_save": "Save Sprites",
        "menu_export": "Export Data File",
        "menu_exit": "Exit",
        "menu_edit": "Edit",
        "menu_view": "View",
        "menu_zoom_in": "Zoom In",
        "menu_zoom_out": "Zoom Out",
        "menu_clear": "Clear",
        "menu_help": "Help",
        "menu_usage": "Usage Guide",
        "menu_about": "About",
        "menu_language": "Language",

        # Toolbar
        "toolbar_open": "Open Image",
        "toolbar_save": "Save Sprites",
        "toolbar_split": "Split",
        "toolbar_clear": "Clear",
        "toolbar_zoom": "Zoom:",
        "toolbar_fit": "Fit",

        # Panels
        "panel_sprite_list": "Sprite List",
        "panel_preview": "Preview",
        "panel_settings": "Settings",

        # Sprite list
        "sprite_count": "{count} sprites",
        "sprite_preview_count": "Preview: {count} sprites",
        "btn_delete": "🗑 Delete",
        "btn_renumber": "🔢 Renumber",

        # Settings panel
        "splitter_title": "SpriteLab",
        "split_mode": "Split Mode",
        "mode_grid": "Grid",
        "mode_rect": "Rectangular",
        "mode_data": "Data File",

        # Grid settings
        "grid_settings": "Grid Settings",
        "grid_columns": "Columns:",
        "grid_rows": "Rows:",
        "sprite_width": "Sprite Width:",
        "sprite_height": "Sprite Height:",
        "padding": "Padding:",
        "margin": "Margin:",

        # Rectangular settings
        "rect_settings": "Rectangular Settings",
        "min_width": "Min Width:",
        "min_height": "Min Height:",
        "alpha_threshold": "Alpha Threshold:",

        # Data file settings
        "data_settings": "Data File Settings",
        "data_file": "Data File:",
        "browse": "Browse",

        # Output settings
        "output_settings": "Output Settings",
        "output_dir": "Output Directory:",
        "name_template": "Name Template:",
        "template_help": "Variables: {name} {index} {x} {y} {width} {height}  e.g. sprite_{index}",
        "format": "Format:",
        "trim_transparent": "Trim Transparent",
        "restore_source": "Restore Source Size",
        "offset_origin": "Offset Origin",
        "offset_origin_top": "Top-Left",
        "offset_origin_bottom": "Bottom-Left",
        "edge_crop": "Edge Crop:",
        "edge_crop_hint": "(Remove border lines)",
        "smart_edge": "Smart Edge Detection",
        "smart_edge_hint": "(Auto detect & remove separator lines)",
        "remove_bg": "Remove Background",
        "remove_bg_hint": "(Remove edge background, keep interior)",
        "btn_apply": "Apply",
        "btn_save_sprites": "💾 Save Sprites",

        # Batch Resize
        "resize_settings": "Batch Resize",
        "resize_mode": "Resize Mode:",
        "resize_none": "No Resize",
        "resize_scale": "By Scale",
        "resize_custom": "Custom Size",
        "scale_ratio": "Scale Ratio:",
        "target_width": "Width:",
        "target_height": "Height:",
        "keep_ratio": "Keep Aspect Ratio",

        # Status Bar
        "status_ready": "Ready",
        "status_loaded": "Loaded: {name}",
        "status_clipboard_loaded": "Loaded from clipboard: {name}",
        "status_split_complete": "Split complete, {count} sprites found",
        "status_saved_to": "Saved {count} sprites to {path}",
        "status_deleted": "Sprite deleted, {count} remaining",
        "status_deleted_all": "Deleted all sprites",
        "status_renumbered": "Renumbered {count} sprites",
        "status_exported": "Data file exported: {path}",
        "status_selected": "Selected: {name} - Pos({x}, {y}) Size({w}x{h})",
        "sprite_count_total": "{count} sprites in total",
        "sprite_count_preview": "Preview: {count} sprites",
        "size_info": "{w} x {h}, {count} sprites",

        # Dialogs
        "warning": "Warning",
        "error": "Error",
        "success": "Success",
        "confirm": "Confirm",
        "info": "Info",

        # Message titles
        "title_warning": "Warning",
        "title_info": "Information",
        "title_error": "Error",
        "title_success": "Success",
        "title_confirm": "Confirm",
        "title_complete": "Complete",

        # Detailed messages
        "msg_clipboard_not_image": "The file in clipboard is not a supported image format",
        "msg_clipboard_help": "Please copy the full path of the image file, or use 'Open Image' button",
        "msg_clipboard_empty": "Clipboard is empty or does not contain a file path\n\nPlease copy the full path",
        "msg_paste_failed": "Paste failed: {error}",
        "msg_load_failed": "Load image failed: {error}",
        "msg_split_failed": "Split failed: {error}",
        "msg_save_failed": "Save failed: {error}",
        "msg_export_failed": "Export failed: {error}",
        "msg_template_applied": "Applied name template to {count} sprites",
        "msg_select_data_first": "Please select a data file first",

        # Messages
        "msg_load_image": "Please load an image first",
        "msg_do_split": "Please split the image first",
        "err_no_image": "Please load an image",
        "err_no_sprites": "Please split first",
        "msg_select_data": "Please select a data file",
        "msg_select_sprite": "Please select a sprite to delete",
        "msg_no_sprites": "No sprites to renumber",
        "msg_delete_all": "Delete all sprites?",
        "msg_save_success": "Saved {count} sprites to:\n{path}",

        # Help
        "help_title": "Usage Guide",
        "about_title": "About",
        "opensource_hint": "Free Version v1.0.11 | SpriteLab.app",

        # Preview hint
        "preview_hint": "Double-click to open image\nor use Cmd+V to paste image path\nor click 'Open Image' button",

        # Help long text
        "help_text": """
Usage Guide:

1. Open Sprite Sheet
   - Drag & drop image to window
   - Paste image path (Cmd+V)
   - Use Open Image shortcut (Cmd+O)

2. Select Split Mode
   - Grid: Fixed grid splitting
   - Rectangular: Auto detect regions by transparent boundaries
   - Data File: Split using JSON data

3. Configure Parameters
   - Grid: Set columns/rows or sprite size
   - Rectangular: Set min size and alpha threshold
   - Data File: Select JSON file

4. Execute Split
   - Click 'Split' button (magnifier icon)
   - Check preview area

5. Save Sprites
   - Click 'Save Sprites' button
   - Configure output dir and name template

Name Template Variables:
{name} - Original filename
{index} - Sprite index
{x}, {y} - Position
{width}, {height} - Size
""",
        "about_text": """
SpriteLab - Sprite Sheet Splitter

Version: {version}
Author: AI Assistant

A simple alternative to TexturePacker,
built with Python + Pillow + tkinter.

Features:
- Grid mode splitting
- Rectangular auto-detection
- Data file splitting
- Real-time preview & zoom
- Sprite highlighting
- Custom output settings
- Multi-language support

Open source & free!
""",

        # Update
        "update_available": "New version: {version}",
        "btn_update": "⬇️ Update",

        # Context menu
        "ctx_delete": "Delete Selected Sprite",
        "ctx_renumber": "Renumber",
        "ctx_delete_all": "Delete All",
    }
}


class I18n:
    """国际化类"""

    def __init__(self, default_lang: str = "zh"):
        self.current_lang = default_lang
        self.listeners = []  # 语言变化监听器

    def get(self, key: str, **kwargs) -> str:
        """获取翻译文本"""
        text = LANGUAGES.get(self.current_lang, LANGUAGES["en"]).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def t(self, key: str, **kwargs) -> str:
        """get的别名"""
        return self.get(key, **kwargs)

    def set_language(self, lang: str):
        """设置语言"""
        if lang in LANGUAGES:
            self.current_lang = lang
            # 通知所有监听器
            for listener in self.listeners:
                listener()

    def get_language(self) -> str:
        """获取当前语言"""
        return self.current_lang

    def add_listener(self, callback):
        """添加语言变化监听器"""
        self.listeners.append(callback)

    def remove_listener(self, callback):
        """移除语言变化监听器"""
        if callback in self.listeners:
            self.listeners.remove(callback)

    def get_available_languages(self) -> dict:
        """获取可用语言列表"""
        return {
            "zh": "中文",
            "en": "English"
        }


# 全局实例
i18n = I18n()
