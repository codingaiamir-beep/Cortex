# Cortex

دستیار مشاورهٔ آموزشی فارسی با بازیابی اطلاعات از پایگاه دانش محلی، حافظهٔ کوتاه‌مدت مکالمه و امتیازدهی لید.

## راه‌اندازی

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

کلید `OPENAI_API_KEY` (یا `OPENROUTER_API_KEY`) را در `.env` قرار دهید و سپس اجرا کنید:

```powershell
python main.py
```

## آزمون

```powershell
python -m unittest -v test_bot.py
```

آزمون‌ها به شبکه یا کلید API نیاز ندارند. فایل `knowledge_base.json` منبع اطلاعات پاسخ‌ها است.
