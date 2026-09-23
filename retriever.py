import json
import os
import re
from typing import Any, Dict, List, Set


class KnowledgeRetriever:
    """
    موتور بازیابی مبتنی بر تطابق کلمات کلیدی، نرمال‌سازی و امتیازدهی وزن‌دار (Heuristic RAG Retriever)
    """
    STOP_WORDS: Set[str] = {
        "این", "آن", "از", "به", "در", "با", "برای", "که", "تا", "را",
        "است", "بود", "شد", "یک", "رو", "تو", "هم", "یا", "و", "چه",
        "کجا", "کی", "آیا", "لطفا", "ممنون", "سلام", "درود"
    }

    SYNONYM_MAP: Dict[str, List[str]] = {
        "قیمت": ["هزینه", "شهریه", "مبلغ", "چقدر", "چنده", "پول", "اقساط", "تخفیف"],
        "گارانتی": ["ضمانت", "بازگشت", "عودت", "مرجوع", "انصراف", "پس"],
        "پشتیبانی": ["ارتباط", "تماس", "مشاوره", "تلفن", "شماره", "ادمین", "تیکت"],
        "ثبت‌نام": ["خرید", "سفارش", "شرکت", "عضویت", "شروع"],
        "دوره": ["کلاس", "ویدیو", "آموزش", "پکیج", "سرفصل"]
    }

    def __init__(self, kb_path: str = "knowledge_base.json"):
        self.kb_path = kb_path
        self.knowledge_base: List[Dict[str, Any]] = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.kb_path):
            print(f"⚠️ هشدار: فایل {self.kb_path} یافت نشد.")
            return []
        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data.get("documents", data.get("item", []))
                return data
        except Exception as e:
            print(f"❌ خطا در خواندن پایگاه دانش: {e}")
            return []

    @staticmethod
    def normalize_text(txt: str) -> str:
        if not txt:
            return ""
        txt = txt.replace("ي", "ی").replace("ك", "ک").replace("ة", "ه")
        txt = re.sub(r"[؟?!.,،؛:«»()\[\]\-—\t\n]+", " ", txt)
        txt = re.sub(r"\s+", " ", txt).strip()
        return txt

    normaliz_text = normalize_text

    def _tokenize_and_expand(self, query: str) -> Set[str]:
        norm_query = self.normalize_text(query)
        raw_tokens = norm_query.split()
        meaningful_tokens = {t for t in raw_tokens if t not in self.STOP_WORDS and len(t) > 1}
        expanded_tokens = set(meaningful_tokens)

        for token in meaningful_tokens:
            for canonical, syn_list in self.SYNONYM_MAP.items():
                if token == canonical or token in syn_list:
                    expanded_tokens.add(canonical)
                    expanded_tokens.update(syn_list)
        return expanded_tokens

    def _calculate_score(self, tokens: set[str], doc: dict[str, Any]) -> float:
        score = 0.0
        title_norm = self.normalize_text(doc.get("title", ""))
        content_norm = self.normalize_text(doc.get("content", ""))
        raw_tags = doc.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [raw_tags]
        tags_norm = [self.normalize_text(str(tag)) for tag in raw_tags]
        for token in tokens:
            for tag in tags_norm:
                if token in tag:
                    score += 5.0
                    break
            if token in title_norm:
                score += 3.0
            if token in content_norm:
                score += 1.0
        return score

    def retrieve(self, query: str, max_results=3, min_score: float = 1.5) -> List[Dict[str, Any]]:
        """
        فیلتر مرتبط‌ترین اسناد بر اساس پرسش کاربر و فیلتر آستانه امتیاز
        """
        tokens = self._tokenize_and_expand(query)
        scored_docs = []
        for doc in self.knowledge_base:
            score = self._calculate_score(tokens, doc)
            if score >= min_score:
                scored_docs.append((score, doc))
        scored_docs.sort(key=lambda item: item[0], reverse=True)
        result = []
        for score, doc in scored_docs[:max_results]:
            result.append({
                "id": doc.get("id"),
                "title": doc.get("title", "بدون عنوان"),
                "content": doc.get("content", ""),
                "score": round(score, 2),
            })
        return result


if __name__ == "__main__":
    kb_path = "knowledge_base.json"
    engine = KnowledgeRetriever(kb_path)
    print(f"✅ {len(engine.knowledge_base)} سند از دیتابیس بارگذاری شد.")
    queries = [
        "قیمت دوره ریاضی چقدره؟",
        "دهم تجربی چی داری؟",
        "سلام حالت چطوره",
        "پکیج کامل تست چیه؟",
        "از چه کلاس‌هایی پشتیبانی می‌کنید",
        "برای دریافت پکیج‌ها باید چیکار کنیم",
    ]
    for q in queries:
        print(f"\n🔍 سوال: «{q}»")
        matches = engine.retrieve(q)
        if not matches:
            print("   توهم‌زدایی: هیچ سندی برنگشت (بی‌اطلاع ربات).")
        else:
            for m in matches:
                print(f"   ✅ {m['title']} | score={m['score']} | id={m['id']}")
