from bot_engine import BotEngine
from schemas import LeadEnricher
from scorer import LeadScorer


def print_banner() -> None:
    print("=" * 65)
    print(" 🧠 به سیستم مشاور تحصیلی هوشمند کورتکس خوش آمدید! ")
    print(" 📌 برای خروج، exit یا خروج را تایپ کنید.")
    print("=" * 65)


def run_interactive_session() -> None:
    print_banner()
    try:
        engine = BotEngine(kb_path="knowledge_base.json")
    except ValueError as error:
        print(f"❌ خطا در راه‌اندازی: {error}")
        return
    enricher = LeadEnricher()
    scorer = LeadScorer()
    print("✅ سیستم آمادهٔ پاسخ‌گویی است.")
    while True:
        try:
            user_input = input("\n👤 شما: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "خروج", "بستن"}:
                print("\n👋 از گفت‌وگو با کورتکس سپاسگزاریم.")
                break
            lead = scorer.calculate_score(enricher.process("guest", user_input))
            response = engine.generate_response(user_input, lead_profile=lead)
            print(f"\n🤖 مشاور کورتکس:\n{response}")
        except KeyboardInterrupt:
            print("\n👋 برنامه متوقف شد.")
            break


if __name__ == "__main__":
    run_interactive_session()
