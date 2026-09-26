import os
import requests
from google import genai

# 1. إعداد مفاتيح التشغيل (تُقرأ تلقائياً من بيئة السيرفر)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # معرف القناة/المجموعة

client = genai.Client(api_key=GEMINI_API_KEY)

# 2. توليد المحتوى/المنتج مدمجاً به رابط استقبال الأموال أوتوماتيكياً
PAYMENT_LINK = "https://paypal.me/yourname"  # أو رابط حسابك البنكي/المحفظة
prompt = f"""
اكتب مقالاً متخصصاً ودليلاً مصغراً حول 'أفضل طرق استغلال الذكاء الاصطناعي في 2026'.
في نهاية المقال، أضف دعوة لشراء النسخة الكاملة عبر هذا الرابط المباشر: {PAYMENT_LINK}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# 3. النشر الأوتوماتيكي المباشر عبر API (بدون تدخل بشري)
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": response.text,
    "parse_mode": "Markdown"
}

publish_response = requests.post(telegram_url, json=payload)

if publish_response.status_code == 200:
    print("✅ تم إنشاء المنتج ونشره آلياً بنسبة 100% دون أي تدخل بشري!")
else:
    print("❌ خطأ في النشر الآلي:", publish_response.text)
