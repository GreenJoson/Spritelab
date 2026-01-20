"""
@input  依赖：urllib.request, json
@output 导出：VersionChecker, CURRENT_VERSION
@pos    版本检查与更新提示

⚠️ 一旦本文件被更新，务必更新以上注释
"""

import threading
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Callable

# 当前版本
CURRENT_VERSION = "v1.0.14"

# API 地址
UPDATE_API_URL = "https://spritelab.app/api/version"

class VersionChecker:
    def __init__(self):
        self._on_update_available: Optional[Callable[[Dict[str, Any]], None]] = None

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """设置发现更新时的回调函数"""
        self._on_update_available = callback

    def check_for_updates(self):
        """检查更新（异步）"""
        thread = threading.Thread(target=self._check_worker, daemon=True)
        thread.start()

    def _check_worker(self):
        """实际执行检查的线程函数"""
        try:
            # 发送请求
            # 设置User-Agent避免某些服务器拒绝
            req = urllib.request.Request(
                UPDATE_API_URL,
                headers={'User-Agent': f'SpriteLab/{CURRENT_VERSION}'}
            )

            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    self._process_response(data)

        except Exception as e:
            # 更新检查失败是可以接受的，静默失败即可
            print(f"Update check failed: {e}")

    def _process_response(self, data: Dict[str, Any]):
        """处理API响应"""
        latest_version = data.get("version")
        if not latest_version:
            return

        # 简单的版本比较 (假设版本号格式为 vX.Y.Z)
        if self._is_newer(latest_version, CURRENT_VERSION):
            if self._on_update_available:
                self._on_update_available(data)

    def _is_newer(self, latest: str, current: str) -> bool:
        """比较版本号"""
        try:
            # 去掉 'v' 前缀
            l_parts = [int(x) for x in latest.lstrip('v').split('.')]
            c_parts = [int(x) for x in current.lstrip('v').split('.')]

            # 补齐长度
            while len(l_parts) < 3: l_parts.append(0)
            while len(c_parts) < 3: c_parts.append(0)

            return l_parts > c_parts
        except:
            return False

# 全局实例
version_checker = VersionChecker()
