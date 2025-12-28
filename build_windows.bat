@echo off
REM Windows 打包脚本 - Sprite Sheet Splitter
REM 使用方法: 在Windows上双击运行此脚本

echo ========================================
echo  Sprite Sheet Splitter Windows 打包脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 创建虚拟环境...
python -m venv venv_win
call venv_win\Scripts\activate.bat

echo [2/4] 安装依赖...
pip install --upgrade pip
pip install pillow pyinstaller

echo [3/4] 开始打包...
pyinstaller --windowed --name "SpriteSheetSplitter" --add-data "sprite_splitter.py;." --add-data "i18n.py;." gui.py

echo [4/4] 打包完成!
echo.
echo ========================================
echo  打包完成!
echo  EXE文件位置: dist\SpriteSheetSplitter\SpriteSheetSplitter.exe
echo ========================================
echo.

pause
