import os
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv
except ImportError: 
    def load_dotenv() -> bool:
        return False

load_dotenv()


class LLMClient:
    """کلاینت سازگار با OpenAI یا OpenRouter، بر اساس کلید تنظیم‌شده."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("API")
        self.api_key = api_key or openrouter_key or openai_key
        if not self.api_key:
            raise ValueError("API key پیدا نشد. OPENAI_API_KEY یا OPENROUTER_API_KEY را در .env تنظیم کنید.")
        self.uses_openrouter = bool(openrouter_key and (api_key is None or api_key == openrouter_key))
        self.model_name = model_name or ("openai/gpt-4o-mini" if self.uses_openrouter else "gpt-4o-mini")
        client_options = {"api_key": self.api_key}
        if self.uses_openrouter:
            client_options["base_url"] = "https://openrouter.ai/api/v1"
        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError("وابستگی‌ها نصب نشده‌اند؛ دستور pip install -r requirements.txt را اجرا کنید.") from error
        self.client = OpenAI(**client_options)

    def generate_reply(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(model=self.model_name, messages=messages, temperature=0.3, max_tokens=500)
            content = response.choices[0].message.content
            return content.strip() if content else "مدل پاسخ متنی معتبری برنگرداند."
        except Exception:
            return "متأسفانه در حال حاضر امکان پاسخ‌گویی وجود ندارد. لطفاً چند دقیقه بعد دوباره تلاش کنید یا با پشتیبانی تماس بگیرید."
