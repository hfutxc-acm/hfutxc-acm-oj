import os
import shutil
from pathlib import Path

# 未来可替换为 MinIO Client
class StorageService:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def save_file(self, source_path: str | Path, dest_rel_path: str):
        """保存文件到存储后端"""
        dest = (self.base_dir / dest_rel_path).resolve()
        
        # 安全检查
        if self.base_dir not in dest.parents:
            raise ValueError("非法的文件存储路径")
            
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest)
        return str(dest_rel_path)
        
    def get_file(self, rel_path: str) -> Path:
        """获取文件的绝对路径（或未来的预签名 URL）"""
        target = (self.base_dir / rel_path).resolve()
        if self.base_dir not in target.parents:
            raise ValueError("非法的文件访问路径")
        return target
        
    def delete_directory(self, rel_dir: str):
        """递归删除目录"""
        target = (self.base_dir / rel_dir).resolve()
        if self.base_dir not in target.parents:
            raise ValueError("非法的删除路径")
            
        if target.exists() and target.is_dir():
            shutil.rmtree(target)
            
    def write_text(self, rel_path: str, content: str, encoding="utf-8"):
        """写入文本文件"""
        dest = (self.base_dir / rel_path).resolve()
        if self.base_dir not in dest.parents:
            raise ValueError("非法的文件访问路径")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding=encoding)

# 默认实例化本地存储，后续可在此处无缝切换为 MinIOStorageService
storage = StorageService(os.environ.get("STORAGE_ROOT", Path(__file__).parent / "data"))
