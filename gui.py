#!/usr/bin/env python3
"""
精灵表拆分器 GUI版本
使用tkinter实现图形界面，模仿TexturePacker的操作体验

功能：
1. 拖放或选择精灵表图片
2. 三种拆分模式（Grid/Rectangular/Data File）
3. 实时预览
4. 自定义输出设置
5. 多语言支持（中文/英文）
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from pathlib import Path

# 导入核心拆分器
from sprite_splitter import SpriteSplitter, SpriteRect

# 导入多语言支持
# 导入多语言支持
from i18n import i18n
# 导入版本检查
from version_checker import version_checker


class SpriteSheetSplitterGUI:
    """精灵表拆分器图形界面"""

    def __init__(self, root: tk.Tk):
        """
        初始化GUI

        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title(i18n.t("app_title"))
        self.root.geometry("1400x850")
        self.root.minsize(1100, 650)

        # 状态变量
        self.image_path: str = ""
        self.splitter: SpriteSplitter = None
        self.preview_image: ImageTk.PhotoImage = None
        self.original_image: Image.Image = None
        self.zoom_level: float = 1.0
        self.selected_sprite_index: int = -1  # 当前选中的精灵索引
        self.canvas_image_id = None  # 画布上的图片ID
        self.image_offset_x: int = 0  # 图片在画布上的X偏移
        self.image_offset_y: int = 0  # 图片在画布上的Y偏移

        # 设置样式
        self._setup_styles()

        # 创建界面
        self._create_menu()
        self._create_toolbar()
        self._create_main_layout()
        self._create_status_bar()

        # 绑定拖放
        self._setup_drag_drop()

    def _setup_styles(self):
        """设置ttk样式"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Info.TLabel', font=('Helvetica', 10))

    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.menubar = menubar # 保存引用以便后续操作

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.t("menu_file"), menu=file_menu)
        file_menu.add_command(label=i18n.t("menu_open"), command=self.open_image, accelerator="Cmd+O")
        file_menu.add_command(label=i18n.t("menu_data"), command=self.open_data_file)
        file_menu.add_separator()
        file_menu.add_command(label=i18n.t("menu_save"), command=self.save_sprites, accelerator="Cmd+S")
        file_menu.add_command(label=i18n.t("menu_export"), command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label=i18n.t("menu_exit"), command=self.root.quit, accelerator="Cmd+Q")

        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.t("menu_edit"), menu=edit_menu)
        edit_menu.add_command(label=i18n.t("toolbar_split"), command=self.do_split)
        edit_menu.add_command(label=i18n.t("menu_clear"), command=self.clear_all)

        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.t("menu_view"), menu=view_menu)
        view_menu.add_command(label=i18n.t("menu_zoom_in"), command=lambda: self.zoom(1.2), accelerator="Cmd++")
        view_menu.add_command(label=i18n.t("menu_zoom_out"), command=lambda: self.zoom(0.8), accelerator="Cmd+-")
        view_menu.add_command(label=i18n.t("toolbar_fit"), command=self.fit_to_window)
        view_menu.add_command(label="1:1", command=lambda: self.set_zoom(1.0))

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.t("menu_help"), menu=help_menu)
        help_menu.add_command(label=i18n.t("menu_usage"), command=self.show_help)
        help_menu.add_command(label=i18n.t("menu_about"), command=self.show_about)

        # 语言菜单
        self.lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=i18n.t("menu_language"), menu=self.lang_menu)

        # 使用变量来标记当前语言
        self.lang_var = tk.StringVar(value=i18n.get_language())
        self.lang_menu.add_radiobutton(label="中文", variable=self.lang_var, value="zh",
                                        command=lambda: self.change_language("zh"))
        self.lang_menu.add_radiobutton(label="English", variable=self.lang_var, value="en",
                                        command=lambda: self.change_language("en"))

        # 绑定快捷键
        self.root.bind('<Command-o>', lambda e: self.open_image())
        self.root.bind('<Command-s>', lambda e: self.save_sprites())
        self.root.bind('<Command-plus>', lambda e: self.zoom(1.2))
        self.root.bind('<Command-minus>', lambda e: self.zoom(0.8))

    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="📂 " + i18n.t("toolbar_open"), command=self.open_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 " + i18n.t("toolbar_save"), command=self.save_sprites).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="🔍 " + i18n.t("toolbar_split"), command=self.do_split).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ " + i18n.t("toolbar_clear"), command=self.clear_all).pack(side=tk.LEFT, padx=2)

        # 缩放控制
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Label(toolbar, text=i18n.t("toolbar_zoom")).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="-", width=3, command=lambda: self.zoom(0.8)).pack(side=tk.LEFT)
        self.zoom_label = ttk.Label(toolbar, text="100%", width=6)
        self.zoom_label.pack(side=tk.LEFT)
        ttk.Button(toolbar, text="+", width=3, command=lambda: self.zoom(1.2)).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="1:1", command=lambda: self.set_zoom(1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="1:1", command=lambda: self.set_zoom(1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=i18n.t("toolbar_fit"), command=self.fit_to_window).pack(side=tk.LEFT, padx=2)

        # 更新按钮（默认隐藏，有更新时显示）
        self.update_btn_frame = ttk.Frame(toolbar)
        self.update_btn_frame.pack(side=tk.RIGHT, padx=10)
        self.update_btn = ttk.Button(
            self.update_btn_frame,
            text=i18n.t("btn_update"),
            command=self.open_update_url,
            style='Accent.TButton'
        )
        # 初始检查更新
        self.root.after(2000, self.check_updates)

    def _create_main_layout(self):
        """创建主布局"""
        # 主分割面板
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧 - 精灵列表
        left_frame = self._create_sprite_list_panel()
        main_paned.add(left_frame, weight=1)

        # 中间 - 预览区域
        center_frame = self._create_preview_panel()
        main_paned.add(center_frame, weight=4)

        # 右侧 - 设置面板（更宽）
        right_frame = self._create_settings_panel()
        main_paned.add(right_frame, weight=2)

    def _create_sprite_list_panel(self) -> ttk.Frame:
        """创建精灵列表面板"""
        frame = ttk.LabelFrame(self.root, text=i18n.t("panel_sprite_list"), padding=5)

        # 精灵列表
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # 列表框和滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sprite_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.sprite_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.sprite_listbox.yview)

        # 绑定选择事件
        self.sprite_listbox.bind('<<ListboxSelect>>', self.on_sprite_select)

        # 绑定删除快捷键
        self.sprite_listbox.bind('<Delete>', self.delete_selected_sprite)
        self.sprite_listbox.bind('<BackSpace>', self.delete_selected_sprite)

        # 右键菜单
        self.sprite_context_menu = tk.Menu(self.sprite_listbox, tearoff=0)
        self.sprite_context_menu.add_command(label=i18n.t("ctx_delete"), command=self.delete_selected_sprite)
        self.sprite_context_menu.add_command(label=i18n.t("ctx_renumber"), command=self.renumber_sprites)
        self.sprite_context_menu.add_separator()
        self.sprite_context_menu.add_command(label=i18n.t("ctx_delete_all"), command=self.delete_all_sprites)

        self.sprite_listbox.bind('<Button-2>', self.show_sprite_context_menu)  # macOS右键
        self.sprite_listbox.bind('<Control-Button-1>', self.show_sprite_context_menu)  # macOS Ctrl+点击

        # 操作按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=2)

        ttk.Button(btn_frame, text=i18n.t("btn_delete"), command=self.delete_selected_sprite, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text=i18n.t("btn_renumber"), command=self.renumber_sprites, width=10).pack(side=tk.LEFT, padx=2)

        # 信息标签
        self.sprite_count_label = ttk.Label(frame, text=i18n.t("sprite_count", count=0), style='Info.TLabel')
        self.sprite_count_label.pack(pady=5)

        return frame

    def _create_preview_panel(self) -> ttk.Frame:
        """创建预览面板"""
        frame = ttk.LabelFrame(self.root, text=i18n.t("panel_preview"), padding=5)

        # 画布容器（支持滚动）
        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # 滚动条
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)

        # 画布 - 使用深灰色棋盘格背景
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='#404040',
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set,
            highlightthickness=0
        )

        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)

        # 布局
        self.canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # 保存canvas_frame引用用于后续获取尺寸
        self.canvas_frame = canvas_frame

        # 提示文本
        self.hint_text = self.canvas.create_text(
            200, 150,
            text=i18n.t("preview_hint"),
            fill='#888888',
            font=('Helvetica', 14),
            justify=tk.CENTER
        )

        # 绑定鼠标事件
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Button-4>', lambda e: self.zoom(1.1))
        self.canvas.bind('<Button-5>', lambda e: self.zoom(0.9))

        # 绑定窗口大小改变事件
        self.canvas.bind('<Configure>', self.on_canvas_resize)

        # 绑定画布点击事件（用于选中精灵）
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        return frame

    def _create_settings_panel(self) -> ttk.Frame:
        """创建设置面板"""
        frame = ttk.LabelFrame(self.root, text=i18n.t("panel_settings"), padding=5)

        # 使用Notebook创建选项卡
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # 精灵表拆分器选项卡
        splitter_frame = ttk.Frame(notebook, padding=10)
        notebook.add(splitter_frame, text=i18n.t("splitter_title"))

        # 拆分模式选择
        mode_frame = ttk.LabelFrame(splitter_frame, text=i18n.t("split_mode"), padding=5)
        mode_frame.pack(fill=tk.X, pady=5)

        self.split_mode = tk.StringVar(value="grid")

        modes_container = ttk.Frame(mode_frame)
        modes_container.pack(fill=tk.X)

        ttk.Radiobutton(modes_container, text=i18n.t("mode_grid"), variable=self.split_mode,
                       value="grid", command=self.on_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(modes_container, text=i18n.t("mode_rect"), variable=self.split_mode,
                       value="rect", command=self.on_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(modes_container, text=i18n.t("mode_data"), variable=self.split_mode,
                       value="data", command=self.on_mode_change).pack(side=tk.LEFT, padx=5)

        # Grid模式设置
        self.grid_frame = ttk.LabelFrame(splitter_frame, text=i18n.t("grid_settings"), padding=5)
        self.grid_frame.pack(fill=tk.X, pady=5)

        # 列数和行数
        grid_row1 = ttk.Frame(self.grid_frame)
        grid_row1.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row1, text="Columns:", width=12).pack(side=tk.LEFT)
        self.columns_var = tk.StringVar(value="1")
        self.columns_var.trace_add("write", self.on_grid_param_change)
        columns_spinbox = ttk.Spinbox(grid_row1, from_=1, to=100, textvariable=self.columns_var, width=8)
        columns_spinbox.pack(side=tk.LEFT)

        grid_row2 = ttk.Frame(self.grid_frame)
        grid_row2.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row2, text="Rows:", width=12).pack(side=tk.LEFT)
        self.rows_var = tk.StringVar(value="1")
        self.rows_var.trace_add("write", self.on_grid_param_change)
        rows_spinbox = ttk.Spinbox(grid_row2, from_=1, to=100, textvariable=self.rows_var, width=8)
        rows_spinbox.pack(side=tk.LEFT)

        # 精灵尺寸
        grid_row3 = ttk.Frame(self.grid_frame)
        grid_row3.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row3, text="精灵宽度:", width=12).pack(side=tk.LEFT)
        self.sprite_width_var = tk.StringVar(value="0")
        self.sprite_width_var.trace_add("write", self.on_grid_param_change)
        sprite_width_spinbox = ttk.Spinbox(grid_row3, from_=0, to=9999, textvariable=self.sprite_width_var, width=8)
        sprite_width_spinbox.pack(side=tk.LEFT)

        grid_row4 = ttk.Frame(self.grid_frame)
        grid_row4.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row4, text="精灵高度:", width=12).pack(side=tk.LEFT)
        self.sprite_height_var = tk.StringVar(value="0")
        self.sprite_height_var.trace_add("write", self.on_grid_param_change)
        sprite_height_spinbox = ttk.Spinbox(grid_row4, from_=0, to=9999, textvariable=self.sprite_height_var, width=8)
        sprite_height_spinbox.pack(side=tk.LEFT)

        # 间距设置
        grid_row5 = ttk.Frame(self.grid_frame)
        grid_row5.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row5, text="形状填充:", width=12).pack(side=tk.LEFT)
        self.padding_var = tk.StringVar(value="0")
        self.padding_var.trace_add("write", self.on_grid_param_change)
        padding_spinbox = ttk.Spinbox(grid_row5, from_=0, to=100, textvariable=self.padding_var, width=8)
        padding_spinbox.pack(side=tk.LEFT)

        grid_row6 = ttk.Frame(self.grid_frame)
        grid_row6.pack(fill=tk.X, pady=2)
        ttk.Label(grid_row6, text="边框填充:", width=12).pack(side=tk.LEFT)
        self.margin_var = tk.StringVar(value="0")
        self.margin_var.trace_add("write", self.on_grid_param_change)
        margin_spinbox = ttk.Spinbox(grid_row6, from_=0, to=100, textvariable=self.margin_var, width=8)
        margin_spinbox.pack(side=tk.LEFT)

        # Rectangular模式设置（默认隐藏）
        self.rect_frame = ttk.LabelFrame(splitter_frame, text="Rectangular设置", padding=5)

        rect_row1 = ttk.Frame(self.rect_frame)
        rect_row1.pack(fill=tk.X, pady=2)
        ttk.Label(rect_row1, text="最小宽度:", width=12).pack(side=tk.LEFT)
        self.min_width_var = tk.StringVar(value="1")
        ttk.Spinbox(rect_row1, from_=1, to=1000, textvariable=self.min_width_var, width=8).pack(side=tk.LEFT)

        rect_row2 = ttk.Frame(self.rect_frame)
        rect_row2.pack(fill=tk.X, pady=2)
        ttk.Label(rect_row2, text="最小高度:", width=12).pack(side=tk.LEFT)
        self.min_height_var = tk.StringVar(value="1")
        ttk.Spinbox(rect_row2, from_=1, to=1000, textvariable=self.min_height_var, width=8).pack(side=tk.LEFT)

        rect_row3 = ttk.Frame(self.rect_frame)
        rect_row3.pack(fill=tk.X, pady=2)
        ttk.Label(rect_row3, text="Alpha阈值:", width=12).pack(side=tk.LEFT)
        self.alpha_threshold_var = tk.StringVar(value="0")
        ttk.Spinbox(rect_row3, from_=0, to=255, textvariable=self.alpha_threshold_var, width=8).pack(side=tk.LEFT)

        # Data File模式设置（默认隐藏）
        self.data_frame = ttk.LabelFrame(splitter_frame, text="数据文件设置", padding=5)

        data_row1 = ttk.Frame(self.data_frame)
        data_row1.pack(fill=tk.X, pady=2)
        self.data_file_var = tk.StringVar(value="")
        ttk.Entry(data_row1, textvariable=self.data_file_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(data_row1, text="浏览", command=self.browse_data_file).pack(side=tk.LEFT, padx=2)

        # 输出设置
        output_frame = ttk.LabelFrame(splitter_frame, text=i18n.t("output_settings"), padding=5)
        output_frame.pack(fill=tk.X, pady=5)

        out_row1 = ttk.Frame(output_frame)
        out_row1.pack(fill=tk.X, pady=2)
        ttk.Label(out_row1, text=i18n.t("output_dir")).pack(side=tk.LEFT)

        out_row2 = ttk.Frame(output_frame)
        out_row2.pack(fill=tk.X, pady=2)
        self.output_dir_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        ttk.Entry(out_row2, textvariable=self.output_dir_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(out_row2, text="📁", command=self.browse_output_dir).pack(side=tk.LEFT)

        out_row3 = ttk.Frame(output_frame)
        out_row3.pack(fill=tk.X, pady=2)
        ttk.Label(out_row3, text=i18n.t("name_template")).pack(side=tk.LEFT)

        out_row4 = ttk.Frame(output_frame)
        out_row4.pack(fill=tk.X, pady=2)
        self.name_template_var = tk.StringVar(value="sprite_{index}")
        ttk.Entry(out_row4, textvariable=self.name_template_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(out_row4, text=i18n.t("btn_apply"), command=self.apply_name_template, width=5).pack(side=tk.LEFT, padx=2)

        # 模板语法说明
        template_help_frame = ttk.Frame(output_frame)
        template_help_frame.pack(fill=tk.X, pady=2)
        template_help = ttk.Label(
            template_help_frame,
            text=i18n.t("template_help"),
            font=('Helvetica', 9),
            foreground='#666666'
        )
        template_help.pack(anchor=tk.W)

        out_row5 = ttk.Frame(output_frame)
        out_row5.pack(fill=tk.X, pady=2)
        ttk.Label(out_row5, text=i18n.t("format")).pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="png")
        format_combo = ttk.Combobox(out_row5, textvariable=self.format_var,
                                    values=["png", "jpg", "webp"], width=8)
        format_combo.pack(side=tk.LEFT, padx=5)

        self.trim_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(out_row5, text=i18n.t("trim_transparent"), variable=self.trim_var).pack(side=tk.LEFT)

        # 边缘裁剪设置
        out_row6 = ttk.Frame(output_frame)
        out_row6.pack(fill=tk.X, pady=2)
        ttk.Label(out_row6, text=i18n.t("edge_crop"), width=10).pack(side=tk.LEFT)
        self.edge_crop_var = tk.StringVar(value="0")
        edge_crop_spinbox = ttk.Spinbox(out_row6, from_=0, to=50, textvariable=self.edge_crop_var, width=5)
        edge_crop_spinbox.pack(side=tk.LEFT)
        ttk.Label(out_row6, text="px", foreground='#666666').pack(side=tk.LEFT, padx=2)
        ttk.Label(out_row6, text=i18n.t("edge_crop_hint"), foreground='#666666', font=('Helvetica', 9)).pack(side=tk.LEFT, padx=5)

        # 智能边缘检测
        out_row7 = ttk.Frame(output_frame)
        out_row7.pack(fill=tk.X, pady=2)
        self.smart_edge_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(out_row7, text=i18n.t("smart_edge"), variable=self.smart_edge_var).pack(side=tk.LEFT)
        ttk.Label(out_row7, text=i18n.t("smart_edge_hint"), foreground='#666666', font=('Helvetica', 9)).pack(side=tk.LEFT, padx=5)

        # 智能去背景
        out_row8 = ttk.Frame(output_frame)
        out_row8.pack(fill=tk.X, pady=2)
        self.remove_bg_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(out_row8, text=i18n.t("remove_bg"), variable=self.remove_bg_var).pack(side=tk.LEFT)
        ttk.Label(out_row8, text=i18n.t("remove_bg_hint"), foreground='#666666', font=('Helvetica', 9)).pack(side=tk.LEFT, padx=5)

        # 批量调整大小设置
        resize_frame = ttk.LabelFrame(splitter_frame, text=i18n.t("resize_settings"), padding=5)
        resize_frame.pack(fill=tk.X, pady=5)

        # 缩放模式选择
        resize_mode_row = ttk.Frame(resize_frame)
        resize_mode_row.pack(fill=tk.X, pady=2)
        ttk.Label(resize_mode_row, text=i18n.t("resize_mode"), width=10).pack(side=tk.LEFT)

        self.resize_mode_var = tk.StringVar(value="none")
        resize_mode_combo = ttk.Combobox(resize_mode_row, textvariable=self.resize_mode_var, width=12, state="readonly")
        resize_mode_combo['values'] = [
            i18n.t("resize_none"),      # 不缩放
            i18n.t("resize_scale"),     # 按比例
            i18n.t("resize_custom"),    # 自定义尺寸
        ]
        resize_mode_combo.current(0)
        resize_mode_combo.pack(side=tk.LEFT, padx=5)
        resize_mode_combo.bind('<<ComboboxSelected>>', self.on_resize_mode_change)

        # 按比例缩放 - 比例选择
        self.scale_frame = ttk.Frame(resize_frame)
        ttk.Label(self.scale_frame, text=i18n.t("scale_ratio"), width=10).pack(side=tk.LEFT)
        self.resize_scale_var = tk.StringVar(value="100")
        scale_combo = ttk.Combobox(self.scale_frame, textvariable=self.resize_scale_var, width=8)
        scale_combo['values'] = ["25", "50", "75", "100", "125", "150", "200", "300", "400"]
        scale_combo.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.scale_frame, text="%").pack(side=tk.LEFT)

        # 自定义尺寸输入
        self.size_frame = ttk.Frame(resize_frame)

        # 宽度输入
        size_row = ttk.Frame(self.size_frame)
        size_row.pack(fill=tk.X, pady=2)
        ttk.Label(size_row, text=i18n.t("target_width"), width=10).pack(side=tk.LEFT)
        self.resize_width_var = tk.StringVar(value="64")
        ttk.Entry(size_row, textvariable=self.resize_width_var, width=6).pack(side=tk.LEFT)
        ttk.Label(size_row, text="px").pack(side=tk.LEFT, padx=(2, 10))

        # 高度输入
        ttk.Label(size_row, text=i18n.t("target_height"), width=10).pack(side=tk.LEFT)
        self.resize_height_var = tk.StringVar(value="64")
        ttk.Entry(size_row, textvariable=self.resize_height_var, width=6).pack(side=tk.LEFT)
        ttk.Label(size_row, text="px").pack(side=tk.LEFT, padx=2)

        # 保持宽高比选项
        ratio_row = ttk.Frame(self.size_frame)
        ratio_row.pack(fill=tk.X, pady=2)
        self.keep_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ratio_row, text=i18n.t("keep_ratio"), variable=self.keep_ratio_var).pack(side=tk.LEFT)


        # 保存按钮
        ttk.Button(splitter_frame, text=i18n.t("btn_save_sprites"), command=self.save_sprites).pack(fill=tk.X, pady=10)

        # 专业版提示（模仿TexturePacker）
        pro_frame = ttk.Frame(frame)
        pro_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        ttk.Label(pro_frame, text=i18n.t("opensource_hint"),
                 foreground='#888888').pack()

        return frame

    def _create_status_bar(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(status_frame, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.size_label = ttk.Label(status_frame, text="", anchor=tk.E)
        self.size_label.pack(side=tk.RIGHT, padx=5)

    def _setup_drag_drop(self):
        """
        设置拖放支持

        支持方式：
        1. tkinterdnd2库（如果安装）
        2. macOS原生拖放
        3. 双击预览区域打开文件选择器
        4. Cmd+V粘贴文件路径
        """
        # 绑定双击事件 - 双击预览区域打开文件选择器
        self.canvas.bind('<Double-Button-1>', lambda e: self.open_image())

        # 绑定Cmd+V粘贴 - 从剪贴板获取文件路径
        self.root.bind('<Command-v>', self.paste_from_clipboard)
        self.root.bind('<Control-v>', self.paste_from_clipboard)  # 兼容Windows

        # 尝试使用tkinterdnd2进行拖放支持
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            # 如果成功导入，尝试注册拖放
            self.canvas.drop_target_register(DND_FILES)
            self.canvas.dnd_bind('<<Drop>>', self.on_drop)
            print("✓ tkinterdnd2 拖放支持已启用")
        except ImportError:
            # 如果没有tkinterdnd2，尝试使用macOS原生支持
            self._setup_macos_drag_drop()

    def _setup_macos_drag_drop(self):
        """设置macOS原生拖放支持"""
        try:
            # 尝试使用macOS的AppleScript来获取拖放文件
            # 这是一个替代方案，通过监听鼠标进入事件
            pass
        except:
            pass

        # 更新提示文本，提示用户可以双击
        self.canvas.delete(self.hint_text)
        self.hint_text = self.canvas.create_text(
            200, 150,
            text=i18n.t("preview_hint"),
            fill='#888888',
            font=('Helvetica', 14),
            justify=tk.CENTER
        )

    def paste_from_clipboard(self, event=None):
        """
        从剪贴板粘贴文件路径

        支持：
        1. 直接粘贴文件路径
        2. macOS Finder复制的文件（尝试解析）
        """
        try:
            # 尝试获取剪贴板内容
            clipboard_content = self.root.clipboard_get()

            # 清理路径
            file_path = clipboard_content.strip()

            # 处理 file:// URL格式
            if file_path.startswith('file://'):
                from urllib.parse import unquote
                file_path = unquote(file_path[7:])

            # 检查文件是否存在
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # 检查是否是图片格式
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    self.load_image(file_path)
                    self.status_label.config(text=f"已从剪贴板加载: {os.path.basename(file_path)}")
                else:
                    messagebox.showwarning("警告", "剪贴板中的文件不是支持的图片格式")
            else:
                # 尝试作为路径处理
                if file_path and not file_path.startswith('/'):
                    # 可能是相对路径或其他内容
                    messagebox.showinfo("提示", "请复制图片文件的完整路径，或直接使用'打开图片'按钮")

        except tk.TclError:
            # 剪贴板为空或不包含文本
            messagebox.showinfo("提示", "剪贴板为空或不包含文件路径\n\n请复制图片文件的完整路径")
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败: {e}")

    def on_drop(self, event):
        """处理拖放事件"""
        file_path = event.data.strip('{}')
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            self.load_image(file_path)

    def open_image(self):
        """打开图片对话框"""
        file_path = filedialog.askopenfilename(
            title="选择精灵表图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)

    def open_data_file(self):
        """打开数据文件对话框"""
        file_path = filedialog.askopenfilename(
            title="选择精灵数据文件",
            filetypes=[
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.data_file_var.set(file_path)
            self.split_mode.set("data")
            self.on_mode_change()

    def browse_data_file(self):
        """浏览数据文件"""
        self.open_data_file()

    def browse_output_dir(self):
        """浏览输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_var.set(dir_path)

    def load_image(self, file_path: str):
        """
        加载图片

        Args:
            file_path: 图片文件路径
        """
        try:
            self.image_path = file_path
            self.splitter = SpriteSplitter(file_path)
            self.original_image = self.splitter.image.copy()

            # 清空精灵列表
            self.sprite_listbox.delete(0, tk.END)
            self.sprite_count_label.config(text="共 0 个精灵")

            # 获取图片尺寸
            w, h = self.original_image.size

            # 根据当前列数行数计算精灵尺寸
            columns = int(self.columns_var.get()) if self.columns_var.get() else 1
            rows = int(self.rows_var.get()) if self.rows_var.get() else 1
            columns = max(1, columns)
            rows = max(1, rows)

            # 设置精灵宽高为自动计算值（根据列数行数）
            sprite_w = w // columns
            sprite_h = h // rows

            # 临时禁用trace以避免多次触发
            # 直接设置值
            self.sprite_width_var.set(str(sprite_w))
            self.sprite_height_var.set(str(sprite_h))

            # 更新状态栏
            self.status_label.config(text=f"已加载: {os.path.basename(file_path)}")
            self.size_label.config(text=f"{w} x {h}")

            # 适应窗口并触发实时预览
            self.fit_to_window()

            # 延迟触发一次实时预览更新
            self.root.after(100, self.on_grid_param_change)

        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {e}")

    def update_preview(self, sprites: list = None, selected_index: int = -1):
        """
        更新预览画布
        模仿TexturePacker的预览效果：蓝色边框、半透明绿色遮罩、选中高亮、居中显示

        使用PIL绘制半透明遮罩，类似PS切片效果

        Args:
            sprites: 可选，要标记的精灵列表
            selected_index: 可选，选中的精灵索引，用于高亮显示
        """
        if not self.original_image:
            return

        # 清除画布
        self.canvas.delete("all")

        # 获取画布尺寸
        self.root.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 600
            canvas_height = 400

        # 创建预览图副本
        preview = self.original_image.copy()

        # 如果有精灵数据，在图片上绘制半透明遮罩
        if sprites:
            from PIL import ImageDraw

            # 创建一个RGBA遮罩层
            overlay = Image.new('RGBA', preview.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            for i, sprite in enumerate(sprites):
                is_selected = (i == selected_index)

                if is_selected:
                    # 选中的精灵：绿色遮罩 + 绿色边框
                    # 填充半透明绿色
                    overlay_draw.rectangle(
                        [sprite.x, sprite.y, sprite.x + sprite.width, sprite.y + sprite.height],
                        fill=(0, 255, 0, 60),  # 半透明绿色
                        outline=(0, 255, 0, 255),  # 绿色边框
                        width=3
                    )
                else:
                    # 普通精灵：半透明绿色遮罩 + 边框
                    # 绘制半透明绿色填充
                    overlay_draw.rectangle(
                        [sprite.x, sprite.y, sprite.x + sprite.width, sprite.y + sprite.height],
                        fill=(0, 200, 100, 40),  # 淡绿色半透明
                        outline=(255, 255, 255, 200),  # 白色边框
                        width=1
                    )

            # 将遮罩合成到预览图上
            preview = Image.alpha_composite(preview.convert('RGBA'), overlay)

        # 应用缩放
        scaled_width = int(self.original_image.width * self.zoom_level)
        scaled_height = int(self.original_image.height * self.zoom_level)

        if self.zoom_level != 1.0:
            preview = preview.resize(
                (scaled_width, scaled_height),
                Image.Resampling.LANCZOS
            )

        # 转换为PhotoImage
        self.preview_image = ImageTk.PhotoImage(preview)

        # 计算居中位置
        self.image_offset_x = max(0, (canvas_width - scaled_width) // 2)
        self.image_offset_y = max(0, (canvas_height - scaled_height) // 2)

        # 绘制图片（居中）
        self.canvas_image_id = self.canvas.create_image(
            self.image_offset_x,
            self.image_offset_y,
            anchor=tk.NW,
            image=self.preview_image
        )

        # 绘制蓝色外边框（类似TexturePacker）
        border_color = '#4488ff'  # 蓝色边框
        border_width = 2
        self.canvas.create_rectangle(
            self.image_offset_x - border_width,
            self.image_offset_y - border_width,
            self.image_offset_x + scaled_width + border_width,
            self.image_offset_y + scaled_height + border_width,
            outline=border_color,
            width=border_width
        )

        # 设置滚动区域
        scroll_x1 = min(0, self.image_offset_x - 50)
        scroll_y1 = min(0, self.image_offset_y - 50)
        scroll_x2 = max(canvas_width, self.image_offset_x + scaled_width + 50)
        scroll_y2 = max(canvas_height, self.image_offset_y + scaled_height + 50)
        self.canvas.config(scrollregion=(scroll_x1, scroll_y1, scroll_x2, scroll_y2))

    def on_mode_change(self):
        """拆分模式改变时的处理"""
        mode = self.split_mode.get()

        # 隐藏所有模式设置框
        self.grid_frame.pack_forget()
        self.rect_frame.pack_forget()
        self.data_frame.pack_forget()

        # 显示对应的设置框
        if mode == "grid":
            self.grid_frame.pack(fill=tk.X, pady=5, after=self.grid_frame.master.winfo_children()[0])
            # 触发一次预览更新
            self.on_grid_param_change()
        elif mode == "rect":
            self.rect_frame.pack(fill=tk.X, pady=5, after=self.grid_frame.master.winfo_children()[0])
        elif mode == "data":
            self.data_frame.pack(fill=tk.X, pady=5, after=self.grid_frame.master.winfo_children()[0])

    def on_grid_param_change(self, *args):
        """
        Grid参数变化时的处理 - 实时预览网格线

        当用户修改Columns、Rows、精灵宽度、精灵高度等参数时，
        自动计算网格并更新预览，无需点击"执行拆分"按钮
        """
        if not self.original_image:
            return

        if self.split_mode.get() != "grid":
            return

        try:
            # 获取参数
            columns = int(self.columns_var.get()) if self.columns_var.get() else 1
            rows = int(self.rows_var.get()) if self.rows_var.get() else 1
            sprite_width = int(self.sprite_width_var.get()) if self.sprite_width_var.get() else 0
            sprite_height = int(self.sprite_height_var.get()) if self.sprite_height_var.get() else 0
            padding = int(self.padding_var.get()) if self.padding_var.get() else 0
            margin = int(self.margin_var.get()) if self.margin_var.get() else 0

            # 确保参数有效
            columns = max(1, columns)
            rows = max(1, rows)

            img_width = self.original_image.width
            img_height = self.original_image.height

            # 计算有效区域（去除边缘间距）
            effective_width = img_width - 2 * margin
            effective_height = img_height - 2 * margin

            # 根据给定参数计算网格
            if sprite_width > 0 and sprite_height > 0:
                # 根据精灵尺寸计算列数和行数（但不修改UI值，只用于预览）
                calc_columns = (effective_width + padding) // (sprite_width + padding) if (sprite_width + padding) > 0 else 1
                calc_rows = (effective_height + padding) // (sprite_height + padding) if (sprite_height + padding) > 0 else 1
            else:
                # 根据列数行数计算精灵尺寸
                calc_columns = columns
                calc_rows = rows
                if columns > 0:
                    sprite_width = (effective_width - padding * (columns - 1)) // columns
                if rows > 0:
                    sprite_height = (effective_height - padding * (rows - 1)) // rows

            # 构建预览用的精灵列表
            preview_sprites = []
            sprite_index = 0

            for row in range(rows):
                for col in range(columns):
                    x = margin + col * (sprite_width + padding)
                    y = margin + row * (sprite_height + padding)

                    # 确保不超出图片边界
                    if x + sprite_width <= img_width and y + sprite_height <= img_height:
                        sprite = SpriteRect(
                            x=x,
                            y=y,
                            width=sprite_width,
                            height=sprite_height,
                            name=f"sprite_{sprite_index:04d}"
                        )
                        preview_sprites.append(sprite)
                        sprite_index += 1

            # 更新预览（但不更新splitter的sprites，那是执行拆分时做的事）
            self.update_preview(preview_sprites, self.selected_sprite_index)

            # 更新精灵计数显示
            self.sprite_count_label.config(text=f"预览: {len(preview_sprites)} 个精灵")
            self.size_label.config(text=f"{img_width} x {img_height}, {len(preview_sprites)} sprites")

        except (ValueError, ZeroDivisionError):
            # 参数无效时只显示图片，不显示网格
            self.update_preview(None, -1)


    def do_split(self):
        """执行拆分操作 - 使用与预览相同的计算逻辑"""
        if not self.splitter:
            messagebox.showwarning("警告", "请先加载图片")
            return

        try:
            mode = self.split_mode.get()

            if mode == "grid":
                # 获取参数
                columns = int(self.columns_var.get()) if self.columns_var.get() else 1
                rows = int(self.rows_var.get()) if self.rows_var.get() else 1
                padding = int(self.padding_var.get()) if self.padding_var.get() else 0
                margin = int(self.margin_var.get()) if self.margin_var.get() else 0

                # 确保参数有效
                columns = max(1, columns)
                rows = max(1, rows)

                img_width = self.original_image.width
                img_height = self.original_image.height

                # 计算有效区域（去除边缘间距）
                effective_width = img_width - 2 * margin
                effective_height = img_height - 2 * margin

                # 根据列数行数计算精灵尺寸（与预览逻辑保持一致）
                sprite_width = (effective_width - padding * (columns - 1)) // columns
                sprite_height = (effective_height - padding * (rows - 1)) // rows

                # 使用计算后的参数执行拆分
                sprites = self.splitter.split_by_grid(
                    columns=columns,
                    rows=rows,
                    sprite_width=0,  # 设为0，让核心方法根据列数行数计算
                    sprite_height=0,
                    padding=padding,
                    margin=margin
                )

            elif mode == "rect":
                min_width = int(self.min_width_var.get())
                min_height = int(self.min_height_var.get())
                alpha_threshold = int(self.alpha_threshold_var.get())

                sprites = self.splitter.split_by_rectangle(
                    min_width=min_width,
                    min_height=min_height,
                    alpha_threshold=alpha_threshold
                )

            elif mode == "data":
                data_file = self.data_file_var.get()
                if not data_file:
                    messagebox.showwarning("警告", "请选择数据文件")
                    return

                sprites = self.splitter.split_by_data_file(data_file)

            # 更新精灵列表
            self.sprite_listbox.delete(0, tk.END)
            for sprite in sprites:
                self.sprite_listbox.insert(tk.END,
                    f"{sprite.name} ({sprite.width}x{sprite.height})")

            # 更新计数
            self.sprite_count_label.config(text=f"共 {len(sprites)} 个精灵")
            self.size_label.config(text=f"{self.original_image.width} x {self.original_image.height}, {len(sprites)} sprites")

            # 更新预览
            self.update_preview(sprites)

            self.status_label.config(text=f"拆分完成，共 {len(sprites)} 个精灵")

        except Exception as e:
            messagebox.showerror("错误", f"拆分失败: {e}")

    def save_sprites(self):
        """保存拆分后的精灵"""
        if not self.splitter or not self.splitter.sprites:
            messagebox.showwarning("警告", "请先执行拆分操作")
            return

        try:
            output_dir = self.output_dir_var.get()
            name_template = self.name_template_var.get()
            format = self.format_var.get()
            trim = self.trim_var.get()
            edge_crop = int(self.edge_crop_var.get()) if self.edge_crop_var.get() else 0
            smart_edge = self.smart_edge_var.get()
            remove_bg = self.remove_bg_var.get()

            # 获取缩放参数
            resize_mode, resize_scale, resize_width, resize_height = self._get_resize_params()

            saved_files = self.splitter.save_sprites(
                output_dir=output_dir,
                name_template=name_template,
                format=format,
                trim=trim,
                edge_crop=edge_crop,
                smart_edge_detect=smart_edge,
                remove_bg=remove_bg,
                resize_mode=resize_mode,
                resize_scale=resize_scale,
                resize_width=resize_width,
                resize_height=resize_height
            )

            # 同时导出数据文件
            data_path = os.path.join(output_dir, '_sprites.json')
            self.splitter.export_data_file(data_path)

            self.status_label.config(text=f"已保存 {len(saved_files)} 个精灵到 {output_dir}")
            messagebox.showinfo("成功", f"已保存 {len(saved_files)} 个精灵到:\n{output_dir}")

        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")

    def _get_resize_params(self):
        """获取缩放参数"""
        mode_text = self.resize_mode_var.get()

        # 根据显示文本确定实际模式
        mode_map = {
            i18n.t("resize_none"): "none",
            i18n.t("resize_scale"): "scale",
            i18n.t("resize_custom"): "custom",
        }

        resize_mode = mode_map.get(mode_text, "none")

        # 如果选择自定义且勾选了保持宽高比，使用fit模式
        if resize_mode == "custom" and self.keep_ratio_var.get():
            resize_mode = "fit"

        try:
            resize_scale = float(self.resize_scale_var.get()) / 100.0  # 百分比转换为小数
        except:
            resize_scale = 1.0

        try:
            resize_width = int(self.resize_width_var.get())
        except:
            resize_width = 0

        try:
            resize_height = int(self.resize_height_var.get())
        except:
            resize_height = 0

        return resize_mode, resize_scale, resize_width, resize_height

    def on_resize_mode_change(self, event=None):
        """缩放模式改变时显示/隐藏相应的输入框"""
        mode_text = self.resize_mode_var.get()

        # 隐藏所有子面板
        self.scale_frame.pack_forget()
        self.size_frame.pack_forget()

        # 根据选择显示对应的输入框
        if mode_text == i18n.t("resize_scale"):
            self.scale_frame.pack(fill=tk.X, pady=2)
        elif mode_text == i18n.t("resize_custom"):
            self.size_frame.pack(fill=tk.X, pady=2)


    def show_sprite_context_menu(self, event):
        """显示右键菜单"""
        try:
            # 选中点击的项
            self.sprite_listbox.selection_clear(0, tk.END)
            index = self.sprite_listbox.nearest(event.y)
            self.sprite_listbox.selection_set(index)
            self.sprite_listbox.activate(index)

            # 显示菜单
            self.sprite_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.sprite_context_menu.grab_release()

    def delete_selected_sprite(self, event=None):
        """删除选中的精灵"""
        if not self.splitter or not self.splitter.sprites:
            return

        selection = self.sprite_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选中要删除的精灵")
            return

        index = selection[0]

        # 从列表中删除
        del self.splitter.sprites[index]

        # 更新列表显示
        self.update_sprite_list()

        # 更新预览
        self.update_preview(self.splitter.sprites)

        # 更新状态
        self.sprite_count_label.config(text=f"共 {len(self.splitter.sprites)} 个精灵")
        self.status_label.config(text=f"已删除精灵，剩余 {len(self.splitter.sprites)} 个")

    def delete_all_sprites(self):
        """删除全部精灵"""
        if not self.splitter or not self.splitter.sprites:
            return

        if messagebox.askyesno("确认", "确定要删除全部精灵吗？"):
            self.splitter.sprites = []
            self.sprite_listbox.delete(0, tk.END)
            self.update_preview(None)
            self.sprite_count_label.config(text="共 0 个精灵")
            self.status_label.config(text="已删除全部精灵")

    def renumber_sprites(self):
        """重新编号精灵（消除断序）"""
        if not self.splitter or not self.splitter.sprites:
            messagebox.showwarning("警告", "没有精灵需要编号")
            return

        # 使用当前名称模板重新编号
        template = self.name_template_var.get()

        for i, sprite in enumerate(self.splitter.sprites):
            # 生成新名称
            new_name = template
            new_name = new_name.replace('{name}', f"sprite_{i:04d}")
            new_name = new_name.replace('{index}', str(i))
            new_name = new_name.replace('{x}', str(sprite.x))
            new_name = new_name.replace('{y}', str(sprite.y))
            new_name = new_name.replace('{width}', str(sprite.width))
            new_name = new_name.replace('{height}', str(sprite.height))

            # 如果模板没有变量，添加索引
            if new_name == template and '{' not in new_name:
                new_name = f"{new_name}_{i}"

            sprite.name = new_name

        # 更新列表显示
        self.update_sprite_list()
        self.status_label.config(text=f"已重新编号 {len(self.splitter.sprites)} 个精灵")

    def apply_name_template(self):
        """应用名称模板 - 更新所有精灵的名称"""
        if not self.splitter or not self.splitter.sprites:
            messagebox.showwarning("警告", "请先执行拆分操作")
            return

        # 调用重新编号功能（使用当前模板）
        self.renumber_sprites()
        messagebox.showinfo("完成", f"已应用名称模板到 {len(self.splitter.sprites)} 个精灵")

    def update_sprite_list(self):
        """更新精灵列表显示"""
        self.sprite_listbox.delete(0, tk.END)

        if self.splitter and self.splitter.sprites:
            for sprite in self.splitter.sprites:
                self.sprite_listbox.insert(tk.END,
                    f"{sprite.name} ({sprite.width}x{sprite.height})")

    def export_data(self):
        """导出数据文件"""
        if not self.splitter or not self.splitter.sprites:
            messagebox.showwarning("警告", "请先执行拆分操作")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存数据文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json")]
        )

        if file_path:
            try:
                self.splitter.export_data_file(file_path)
                self.status_label.config(text=f"数据文件已导出: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")

    def clear_all(self):
        """清除所有"""
        self.image_path = ""
        self.splitter = None
        self.original_image = None
        self.preview_image = None

        self.canvas.delete("all")
        self.hint_text = self.canvas.create_text(
            200, 150,
            text=i18n.t("preview_hint"),
            fill='#888888',
            font=('Helvetica', 14),
            justify=tk.CENTER
        )

        self.sprite_listbox.delete(0, tk.END)
        self.sprite_listbox.delete(0, tk.END)
        self.sprite_count_label.config(text=i18n.t("sprite_count", count=0))
        self.status_label.config(text="就绪")
        self.size_label.config(text="")

    def on_sprite_select(self, event):
        """精灵选择事件处理 - 更新选中状态并重绘预览"""
        selection = self.sprite_listbox.curselection()
        if selection and self.splitter and self.splitter.sprites:
            index = selection[0]
            self.selected_sprite_index = index
            sprite = self.splitter.sprites[index]
            self.status_label.config(
                text=f"选中: {sprite.name} - 位置({sprite.x}, {sprite.y}) 尺寸({sprite.width}x{sprite.height})"
            )
            # 重绘预览以显示选中高亮
            self.update_preview(self.splitter.sprites, self.selected_sprite_index)
        else:
            self.selected_sprite_index = -1

    def zoom(self, factor: float):
        """
        缩放

        Args:
            factor: 缩放因子
        """
        self.zoom_level *= factor
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        sprites = self.splitter.sprites if self.splitter else None
        self.update_preview(sprites, self.selected_sprite_index)

    def set_zoom(self, level: float):
        """
        设置缩放级别

        Args:
            level: 缩放级别
        """
        self.zoom_level = level
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        sprites = self.splitter.sprites if self.splitter else None
        self.update_preview(sprites, self.selected_sprite_index)

    def fit_to_window(self):
        """适应窗口大小，保持图片居中"""
        if not self.original_image:
            return

        # 获取画布大小
        self.root.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        # 计算缩放比例
        img_width = self.original_image.width
        img_height = self.original_image.height

        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height

        self.zoom_level = min(scale_x, scale_y) * 0.85  # 留边距
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        sprites = self.splitter.sprites if self.splitter else None
        self.update_preview(sprites, self.selected_sprite_index)

    def on_canvas_resize(self, event):
        """画布大小改变时重新居中图片"""
        if self.original_image:
            sprites = self.splitter.sprites if self.splitter else None
            self.update_preview(sprites, self.selected_sprite_index)

    def on_canvas_click(self, event):
        """
        画布点击事件 - 根据点击位置选中精灵

        Args:
            event: 点击事件
        """
        if not self.splitter or not self.splitter.sprites:
            return

        # 获取点击位置（考虑滚动偏移）
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # 转换为图片坐标
        img_x = (canvas_x - self.image_offset_x) / self.zoom_level
        img_y = (canvas_y - self.image_offset_y) / self.zoom_level

        # 查找点击的精灵
        for i, sprite in enumerate(self.splitter.sprites):
            if (sprite.x <= img_x <= sprite.x + sprite.width and
                sprite.y <= img_y <= sprite.y + sprite.height):
                # 选中该精灵
                self.selected_sprite_index = i

                # 更新列表选中状态
                self.sprite_listbox.selection_clear(0, tk.END)
                self.sprite_listbox.selection_set(i)
                self.sprite_listbox.see(i)  # 滚动到可见

                # 更新状态栏
                self.status_label.config(
                    text=f"选中: {sprite.name} - 位置({sprite.x}, {sprite.y}) 尺寸({sprite.width}x{sprite.height})"
                )

                # 重绘预览
                self.update_preview(self.splitter.sprites, self.selected_sprite_index)
                return

        # 没有点击到任何精灵，取消选中
        self.selected_sprite_index = -1
        self.sprite_listbox.selection_clear(0, tk.END)
        self.update_preview(self.splitter.sprites, -1)

    def on_mouse_wheel(self, event):
        """鼠标滚轮事件"""
        if event.delta > 0:
            self.zoom(1.1)
        else:
            self.zoom(0.9)

    def show_help(self):
        """显示帮助"""
        messagebox.showinfo(i18n.t("help_title"), i18n.t("help_text"))

    def show_about(self):
        """显示关于"""
        from version_checker import CURRENT_VERSION
        messagebox.showinfo(i18n.t("about_title"), i18n.t("about_text", version=CURRENT_VERSION))

    def check_updates(self):
        """检查更新"""
        def on_update_found(data):
            # 在主线程更新UI
            self.update_data = data
            version = data.get('version', '')
            self.root.after(0, lambda: self._show_update_ui(version))

        version_checker.set_callback(on_update_found)
        version_checker.check_for_updates()

    def _show_update_ui(self, version):
        """显示更新UI"""
        self.update_btn.configure(text=f"{i18n.t('btn_update')} {version}")
        self.update_btn.pack(side=tk.RIGHT)

        # 状态栏提示
        msg = i18n.t('update_available', version=version)
        self.status_label.config(text=msg, foreground='blue')

    def open_update_url(self):
        """打开更新链接"""
        url = "https://spritelab.app"
        if hasattr(self, 'update_data') and self.update_data.get('download_url'):
            url = self.update_data['download_url']

        import webbrowser
        webbrowser.open(url)


    def change_language(self, lang: str):
        """切换语言"""
        i18n.set_language(lang)

        # 保存语言配置到用户目录
        save_language_config(lang)

        # 实时更新Canvas提示文本
        if self.hint_text:
            self.canvas.itemconfig(self.hint_text, text=i18n.t("preview_hint"))

        # 刷新菜单
        self._create_menu()

        # 更新标题
        self.root.title(i18n.t("app_title"))

        # 提示用户需要重启应用
        # 提示用户需要重启应用
        # if lang == "zh":
        #     msg = "语言已切换为中文。\n\n部分界面需要重启应用后生效。\n\n是否现在重启？"
        #     title = "语言切换"
        # else:
        #     msg = "Language changed to English.\n\nSome UI changes require restart.\n\nRestart now?"
        #     title = "Language Changed"

        # if messagebox.askyesno(title, msg):
        #     # 重启应用
        #     self.root.destroy()
        #     python = sys.executable
        #     os.execl(python, python, *sys.argv)

def get_config_path():
    """获取配置文件路径 - 使用用户目录"""
    config_dir = os.path.join(os.path.expanduser("~"), ".sprite_sheet_splitter")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.txt")


def load_language_config():
    """加载语言配置"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                lang = f.read().strip()
                if lang in ['zh', 'en']:
                    i18n.set_language(lang)
                    return lang
        except:
            pass
    return "zh"  # 默认中文


def save_language_config(lang: str):
    """保存语言配置"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as f:
            f.write(lang)
    except:
        pass



def main(image_path: str = None):
    """
    主函数

    Args:
        image_path: 可选，启动时自动加载的图片路径
    """
    # 加载语言配置
    load_language_config()

    root = tk.Tk()
    app = SpriteSheetSplitterGUI(root)

    # 如果提供了图片路径，自动加载
    if image_path and os.path.exists(image_path):
        root.after(100, lambda: app.load_image(image_path))

    root.mainloop()

if __name__ == '__main__':
    import sys

    # 支持的图片格式
    SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

    # 支持命令行参数传入图片路径
    # 使用方法: python gui.py [图片路径]
    # 或将图片拖放到脚本文件上
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        # 只有当路径存在且是支持的图片格式时才尝试加载
        if os.path.exists(image_path) and image_path.lower().endswith(SUPPORTED_FORMATS):
            main(image_path)
        else:
            # 不是图片文件，正常启动
            main()
    else:
        main()
