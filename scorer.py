from schemas import LeadProfile, LeadEnricher

class LeadScorer:
    def __init__(self):

        self.weights = {
            "phone_number": 35.0,
            "purchase_intent": 25.0,
            "grade": {
                "دوازدهم": 20.0,
                "فارغ‌التحصیل": 20.0,
                "یازدهم": 15.0,
                "دهم": 10.0,
            },
            "major": 10.0,
            "interaction": 10.0,
        }

    def calculate_score(self, lead: LeadProfile) -> LeadProfile:
        score = 0.0


        if lead.phone_number:
            score += self.weights["phone_number"]


        if lead.purchase_intent:
            score += self.weights["purchase_intent"]


        if lead.grade:
            grade_scores = self.weights["grade"]
            score += grade_scores.get(lead.grade, 0.0)


        if lead.major:
            score += self.weights["major"]


        if lead.message_count > 1:
            score += self.weights["interaction"]


        if score >= 70.0:
            status = "Hot"
        elif score >= 40.0:
            status = "Warm"
        else:
            status = "Cold"

        # به‌روزرسانی پرونده لید
        lead.lead_score = score
        lead.lead_status = status
        return lead


if __name__ == "__main__":
    enricher = LeadEnricher()
    scorer = LeadScorer()

    sample_text = "سلام، دوازدهم تجربی هستم، هزینه پکیج چنده؟ 09121234567"

    raw_lead = enricher.process(user_id="user_101", text=sample_text)
    final_lead = scorer.calculate_score(raw_lead)

    print("--- نتیجه لید نهایی ---")
    print(f"امتیاز: {final_lead.lead_score} از 100")
    print(f"وضعیت: {final_lead.lead_status}")
    print(f"رشته و پایه: {final_lead.grade} - {final_lead.major}")
    print(f"شماره تماس: {final_lead.phone_number}")
