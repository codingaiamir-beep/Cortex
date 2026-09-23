"""تست‌های واحد پایپ‌لاین؛ اجرای آن‌ها نیاز به API key یا شبکه ندارد."""

import unittest
from unittest.mock import patch

from bot_engine import BotEngine
from memory_manage import ConversationMemory
from retriever import KnowledgeRetriever
from schemas import LeadEnricher
from scorer import LeadScorer


class CortexTests(unittest.TestCase):
    def test_retriever_finds_math_course(self):
        documents = KnowledgeRetriever("knowledge_base.json").retrieve("قیمت دوره ریاضی چقدر است؟")
        self.assertEqual(documents[0]["id"], "course_math_comprehensive")

    def test_memory_keeps_only_configured_messages(self):
        memory = ConversationMemory(max_messages=2)
        memory.user_message("اول")
        memory.ai_message("پاسخ اول")
        memory.user_message("دوم")
        self.assertEqual([message["content"] for message in memory.get_history()], ["پاسخ اول", "دوم"])

    def test_lead_enrichment_and_scoring(self):
        lead = LeadEnricher().process("u1", "دوازدهم تجربی هستم؛ هزینه پکیج چنده؟ 09121234567")
        scored = LeadScorer().calculate_score(lead)
        self.assertEqual(scored.lead_status, "Hot")
        self.assertEqual(scored.lead_score, 90.0)

    @patch("bot_engine.LLMClient")
    def test_engine_builds_messages_and_stores_reply(self, mock_client):
        mock_client.return_value.generate_reply.return_value = "پاسخ آزمایشی"
        engine = BotEngine(kb_path="knowledge_base.json")
        reply = engine.generate_response("هزینه دوره ریاضی چقدر است؟")
        self.assertEqual(reply, "پاسخ آزمایشی")
        self.assertEqual(engine.memory.get_history()[-1]["role"], "assistant")


if __name__ == "__main__":
    unittest.main()
