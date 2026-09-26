import os
import time
import requests
import google.generativeai as genai

def main():
    print("🚀 بدء تشغيل محرك Nexus Labs المستقل...")

    # 1. جلب المفاتيح السرية من GitHub Secrets
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not all([bot_token, chat_id, gemini_key]):
        print("❌ خطأ: تأكد من إضافة المفاتيح في GitHub Secrets.")
        exit(1)

    # 2. إعداد Gemini API (باستخدام الموديل السريع والمستقر)
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # التوجيه (Prompt) المؤسسي لـ Nexus Labs
    prompt = """
    بصفتك الذكاء الاصطناعي المؤسسي لـ 'Nexus Labs'..
    اكتب منشوراً واحداً قصيراً واحترافياً باللغة العربية لزوار قناتنا على تيليجرام.
    الموضوع: أهمية بناء أنظمة رقمية تعمل بـ (Zero-Human Loop) لتحقيق أرباح مستقلة.
    الأسلوب: حاد، مباشر، قيم، ومؤسسي. تجنب استخدام الإيموجي بشكل مبالغ فيه.
    """

    # 3. توليد المحتوى مع نظام حماية (Retry Mechanism) لتجنب أخطاء 429
    print("🤖 جاري توليد المحتوى عبر Gemini...")
    post_content = ""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            post_content = response.text
            print("✅ تم توليد المحتوى بنجاح.")
            break # الخروج من حلقة التكرار عند النجاح
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ محاولة {attempt + 1} فشلت: {error_msg}")
            # إذا كان الخطأ بسبب الضغط على السيرفر، انتظر وحاول مجدداً
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                print("⏳ سيرفر جوجل مزدحم (Rate Limit). ننتظر 15 ثانية قبل المحاولة التالية...")
                time.sleep(15)
            else:
                print("❌ حدث خطأ برمجي غير متوقع في Gemini.")
                exit(1)
    
    if not post_content:
        print("❌ فشل النظام في توليد المحتوى بعد 3 محاولات.")
        exit(1)

    # 4. إرسال المحتوى إلى قناة تيليجرام
    print("📨 جاري الإرسال إلى قناة تيليجرام...")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": post_content,
        "parse_mode": "Markdown" # لدعم الخط العريض والمائل
    }

    tg_response = requests.post(telegram_url, json=payload)
    
    if tg_response.status_code == 200:
        print("🏆 تمت المهمة بنجاح! المنشور الآن متاح في قناة Nexus Labs.")
    else:
        print(f"❌ فشل النشر على تيليجرام: {tg_response.text}")
        exit(1)

if __name__ == "__main__":
    main()
