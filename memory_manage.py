from collections import deque
from typing import Any,Set,List,Dict

class ConversationMemory:
    """
    مدیریت حافظه کوتاه‌مدت مکالمه با الگوی پنجره لغزان (Sliding Window).
    این کلاس پیام‌ها را در قالب استاندارد OpenAI ذخیره می‌کند.
    """
    def __init__(self,max_messages:int = 6):
        """
        :param max_messages: حداکثر تعداد پیام‌های ذخیره‌شده (رفت و برگشت‌ها).
        مثلاً عدد ۶ یعنی ۳ پیام کاربر و ۳ پیام ربات.
        """
        self.max_messages = max_messages
        self.history : deque[Dict[str,str]] = deque(maxlen=max_messages)
        
    def user_message(self,message:str) -> None:
        """ثبت پیام ورودی کاربر (رفت)"""
        self.history.append({
            "role" : "user",
            "content" : message.strip()
        })      
        
    def ai_message(self,message:str) -> None:
        """ثبت پاسخ تولید شده توسط ربات (برگشت)"""
        self.history.append({
            "role" : "assistant",
            "content" : message.strip()
        })

    def get_history(self) -> List[Dict[str,str]]:
        """دریافت کل تاریخچه پیام‌های معتبر به صورت لیست"""
        return list(self.history)
    
    def clear(self) -> None:
        """پاکسازی حافظه (برای ریست کردن مکالمه کاربر)"""
        self.history.clear()
# ---------------------------------------------------------
# بلاک تست سلامت مستقل ماژول (Isolation Health Check)
# ---------------------------------------------------------
if __name__ == "__main__":
        print("=== تست سلامت ماژول ConversationMemory ===")
        mem = ConversationMemory(max_messages=4)
        mem.user_message("سلام دوره برنامه نویسی پایتونتون در کدوم بخش اراعه میشه") 
        mem.ai_message("در بخش ماشین لرنینگ ")
        mem.user_message("این دوره چند جلسه ایی است")
        mem.ai_message("این دوره 20 جلسه و هر جلسه به مدت 1 ساعت است")
        print(f"\nتعداد پیام‌ها در حافظه: {len(mem.get_history())}")
        mem.user_message("و مدرس این دوره ها کدوم استاده؟")
        print("\nپیام‌های باقی‌مانده در حافظه بعد از ورود پیام پنجم:")
        
        for msg in mem.get_history():
            print(f"[{msg['role']}]: {msg['content']}")
