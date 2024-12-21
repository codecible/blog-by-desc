import json
import os
import time
from typing import Optional, Any
from ..config import Config

class Cache:
    """缓存管理器"""
    
    def __init__(self):
        self.config = Config()
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{key}.json")
        
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if not self.config.CACHE_ENABLED:
            return None
            
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return None
            
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] > self.config.CACHE_EXPIRE_TIME:
                    os.remove(cache_path)
                    return None
                return data['value']
        except Exception:
            return None
            
    def set(self, key: str, value: Any) -> None:
        """设置缓存数据"""
        if not self.config.CACHE_ENABLED:
            return
            
        cache_path = self._get_cache_path(key)
        data = {
            'timestamp': time.time(),
            'value': value
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 