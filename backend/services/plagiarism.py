import os
import tempfile
import asyncio
from copydetect import CopyDetector

class PlagiarismService:
    def __init__(self, data_dir="/tmp/plagiarism"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            
    async def run_detection(self, reference_codes: list[str], target_code: str, extensions: list[str] = ["cpp", "c", "py", "java"]) -> dict:
        """
        运行代码查重。
        reference_codes: 已经 AC 的其他人提交的代码。
        target_code: 当前目标提交的代码。
        """
        # copydetect 基于文件系统，所以我们需要创建临时文件
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_run_detection, reference_codes, target_code, extensions)
        
    def _sync_run_detection(self, reference_codes: list[str], target_code: str, extensions: list[str]) -> dict:
        if not reference_codes:
            return {"max_similarity": 0, "details": []}
            
        with tempfile.TemporaryDirectory() as ref_dir, tempfile.TemporaryDirectory() as test_dir:
            # 写入 reference_codes
            for i, code in enumerate(reference_codes):
                with open(os.path.join(ref_dir, f"ref_{i}.cpp"), "w", encoding="utf-8") as f:
                    f.write(code)
                    
            # 写入 target_code
            target_file_path = os.path.join(test_dir, "target.cpp")
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(target_code)
                
            detector = CopyDetector(test_dirs=[test_dir], ref_dirs=[ref_dir], extensions=extensions, display_t=0.5)
            detector.run()
            
            # 分析结果
            similarity_data = detector.similarity_matrix
            if not similarity_data or len(similarity_data) == 0:
                return {"max_similarity": 0, "details": []}
                
            # 简化：找到最大相似度
            max_sim = 0
            for test_file, test_results in detector.similarity_matrix.items():
                for ref_file, sim_score in test_results.items():
                    if sim_score[0] > max_sim:  # index 0 is token similarity
                        max_sim = sim_score[0]
                        
            return {
                "max_similarity": max_sim,
                "is_plagiarized": max_sim > 0.8  # 大于 80% 判定为高度嫌疑
            }

plagiarism_service = PlagiarismService()
