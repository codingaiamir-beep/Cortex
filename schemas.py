import re
from typing import Optional
from pydantic import BaseModel


class LeadProfile(BaseModel):
    user_id: str
    phone_number: Optional[str] = None
    grade: Optional[str] = None
    major: Optional[str] = None
    purchase_intent: bool = False
    raw_message: str
    message_count: int = 1
    lead_score: float = 0.0
    lead_status: str = "Cold"


class LeadEnricher:
    def __init__(self):

        self.grade_patterns = {
            "دوازدهم": r"(دوازدهم|۱۲|12|کنکوری)",
            "یازدهم": r"(یازدهم|۱۱|11)",
            "دهم": r"(دهم|۱۰|10)",
            "فارغ‌التحصیل": r"(فارغ\s*التحصیل|پشت\s*کنکور)",
        }


        self.major_patterns = {
            "تجربی": r"(تجربی)",
            "ریاضی": r"(ریاضی|مهندسی)",
            "انسانی": r"(انسانی)",
            "هنر": r"(هنر)",
            "منحصرا زبان": r"(زبان)",
        }

        # کلمات کلیدی قصد خرید
        self.intent_keywords = [
            "قیمت",
            "هزینه",
            "چنده",
            "پکیج",
            "ثبت نام",
            "خرید",
            "مشاوره خصوصی",
            "تعرفه",
        ]

    def extract_grade(self, text: str) -> Optional[str]:
        for grade, pattern in self.grade_patterns.items():
            if re.search(pattern, text):
                return grade
        return None

    def extract_major(self, text: str) -> Optional[str]:
        for major, pattern in self.major_patterns.items():
            if re.search(pattern, text):
                return major
        return None

    def extract_intent(self, text: str) -> bool:
        return any(keyword in text for keyword in self.intent_keywords)

    def process(self, user_id: str, text: str) -> LeadProfile:

        phone_match = re.search(r"09\d{9}", text)
        phone_number = phone_match.group() if phone_match else None

        grade = self.extract_grade(text)
        major = self.extract_major(text)
        purchase_intent = self.extract_intent(text)

        return LeadProfile(
            user_id=user_id,
            phone_number=phone_number,
            grade=grade,
            major=major,
            purchase_intent=purchase_intent,
            raw_message=text,  
            message_count=1,
        )
