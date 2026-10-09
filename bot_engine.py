from typing import Dict, List, Optional

from LLM_client import LLMClient
from memory_manage import ConversationMemory
from retriever import KnowledgeRetriever
from schemas import LeadProfile


class BotEngine:
    """هماهنگ‌کنندهٔ بازیابی دانش، حافظهٔ مکالمه و مدل زبانی."""

    def __init__(self, kb_path: str = "knowledge_base.json", max_history: int = 6, model_name: Optional[str] = None):
        self.retriever = KnowledgeRetriever(kb_path=kb_path)
        self.memory = ConversationMemory(max_messages=max_history)
        self.llm_client = LLMClient(model_name=model_name)

    @staticmethod
    def _format_context(documents: List[Dict[str, str]]) -> str:
        if not documents:
            return "اطلاعاتی یافت نشد."
        return "\n\n".join(f"[سند {index}]\nعنوان: {doc['title']}\nمحتوا: {doc['content']}" for index, doc in enumerate(documents, 1))

    def _build_system_prompt(self, user_query: str, lead_profile: Optional[LeadProfile] = None) -> str:
        relevant_docs = self.retriever.retrieve(query=user_query, max_results=3)
        profile_hint = ""
        if lead_profile:
            details = [value for value in (lead_profile.grade, lead_profile.major) if value]
            if details:
                profile_hint = f"\n[اطلاعات دانش‌آموز]: {'، '.join(details)}\n"
        return f"""شما «کورتکس» هستید، یک مشاور آموزشی و فروش دقیق و حرفه‌ای.

[دستورالعمل‌ها]:
۱. فقط بر اساس اطلاعات پایگاه دانش زیر پاسخ دهید.
۲. اگر پاسخ در اطلاعات نبود، صادقانه بگویید اطلاعات کافی ندارید و حدس نزنید.
۳. لحن شما صمیمی، محترمانه، خلاصه و مفید باشد.
{profile_hint}
[اطلاعات پایگاه دانش]:
{self._format_context(relevant_docs)}
"""

    def prepare_messages(self, user_query: str, lead_profile: Optional[LeadProfile] = None) -> List[Dict[str, str]]:
        query = user_query.strip()
        if not query:
            raise ValueError("پیام کاربر نباید خالی باشد.")
        return [
            {"role": "system", "content": self._build_system_prompt(query, lead_profile)},
            *self.memory.get_history(),
            {"role": "user", "content": query},
        ]

    def generate_response(self, user_query: str, lead_profile: Optional[LeadProfile] = None) -> str:
        messages = self.prepare_messages(user_query, lead_profile)
        ai_reply = self.llm_client.generate_reply(messages)
        self.memory.user_message(user_query)
        self.memory.ai_message(ai_reply)
        return ai_reply

if __name__ == "__main__":
    engine = BotEngine()
    print("کورتکس آماده است. برای خروج بنویس: exit")
    while True:
        user_input = input("شما: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue
        print("کورتکس:", engine.generate_response(user_input))