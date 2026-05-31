import ahocorasick
import os

class SensitiveWordsFilter:
    def __init__(self):
        self.automaton = ahocorasick.Automaton()
        self.is_built = False
        self._load_words()
        
    def _load_words(self):
        # 预设的一些违禁词示例
        default_words = [
            "暴力", "代写", "包过", "涉政", "脚本刷题"
        ]
        
        words = default_words
        
        # 可选：从文件中加载
        word_file = os.path.join(os.path.dirname(__file__), "sensitive_words.txt")
        if os.path.exists(word_file):
            with open(word_file, "r", encoding="utf-8") as f:
                file_words = [line.strip() for line in f if line.strip()]
                words.extend(file_words)
                
        for idx, word in enumerate(set(words)):
            self.automaton.add_word(word, (idx, word))
            
        if len(words) > 0:
            self.automaton.make_automaton()
            self.is_built = True
            
    def contains_sensitive_words(self, text: str) -> bool:
        if not self.is_built or not text:
            return False
            
        for _, _ in self.automaton.iter(text):
            return True
        return False
        
    def filter_text(self, text: str, replace_char: str = "*") -> str:
        if not self.is_built or not text:
            return text
            
        result = text
        for end_idx, (insert_order, original_word) in self.automaton.iter(text):
            start_idx = end_idx - len(original_word) + 1
            result = result[:start_idx] + (replace_char * len(original_word)) + result[end_idx+1:]
        return result

# 全局单例
filter_service = SensitiveWordsFilter()
