import os
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

class AIAssistantService:
    def __init__(self):
        # 兼容 OpenAI 规范的 API
        # 默认使用 DeepSeek 或者是通用的 OpenAI 地址
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        
        self.client = None
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
    async def get_rubber_duck_hint(self, problem_description: str, user_code: str, language: str) -> str:
        """
        小黄鸭调试法助教：不直接给答案，而是通过提问和分析引导选手找到代码的问题。
        """
        if not self.client:
            return "AI 助教尚未配置 (请设置 OPENAI_API_KEY 环境变量)。"
            
        system_prompt = (
            "你是一个名为'小黄鸭'的 ACM/ICPC 算法竞赛助教。"
            "你的目标是引导学生自己发现代码中的逻辑错误、边界条件或时间复杂度问题，而不是直接给出正确的代码。"
            "语气应该温和、鼓励，像一个真正的橡胶鸭子在倾听，并适时提出尖锐的启发式问题。"
            "请用中文回答，并尽量简短，控制在 150 字以内。"
        )
        
        user_message = (
            f"题目描述: {problem_description}\n\n"
            f"我的提交 ({language}):\n"
            f"```\n{user_code}\n```\n"
            "一直 WA (Wrong Answer)，我可能忽略了哪些情况？"
        )
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI Assistant Error: {e}")
            return "小黄鸭正在休息，请稍后再试或向队友求助。"

ai_service = AIAssistantService()
