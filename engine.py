import os
import requests
import google.generativeai as genai

# 1. إعداد مفاتيح الربط والبيئات المستقبلة من GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_OR_STORE_LINK = os.getenv("MY_STORE_LINK") # رابط متجرك أو رابط التسويق بالعمولة الخاص بك

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def run_autonomous_loop():
    print("[+] بدء حلقة الذكاء الاصطناعي المستقلة...")

    # ----------------------------------------------------
    # Agent 1: Strategy & Idea Generation (وكيل الفكرة والقيمة)
    # ----------------------------------------------------
    prompt_agent1 = (
        "You are an expert business strategist. Generate a high-value niche topic "
        "for today. It must alternate between a Digital Product (e-book concept), "
        "a Service (ready code snippet/template), or a Consultation guide. "
        "Crucial: The topic must be 100% ethical, useful, and compliant with Islamic Sharia "
        "(No interest/usury, no adult content, no music/gambling, pure useful knowledge). "
        "Output ONLY the title and the type (Product, Service, or Consultation) in one line."
    )
    response_agent1 = model.generate_content(prompt_agent1).text
    print(f"[Agent 1] الفكرة المقترحة: {response_agent1}")

    # ----------------------------------------------------
    # Agent 2: Content & Value Creation (وكيل الإنشاء والتنفيذ)
    # ----------------------------------------------------
    prompt_agent2 = (
        f"You are an expert content creator and technical writer. Based on this chosen topic: '{response_agent1}', "
        "create a comprehensive, deeply detailed, and valuable guide or output in Arabic. "
        "Provide immediate actionable value to the reader. Structure it with professional sections, "
        "clear steps, and actionable advice. Make it comprehensive so it acts as a standalone free/premium asset."
    )
    response_agent2 = model.generate_content(prompt_agent2).text
    print("[Agent 2] تم توليد المحتوى والقيمة بنجاح.")

    # ----------------------------------------------------
    # Agent 3: Sharia & Quality Compliance (وكيل المراجعة والجودة الفقهية)
    # ----------------------------------------------------
    prompt_agent3 = (
        f"You are a strict quality control auditor and Islamic Sharia compliance expert. Review the following content:\n\n"
        f"{response_agent2}\n\n"
        "Ensure there is absolutely NO forbidden content, misleading claims, or low-quality text. "
        "If it is fully compliant and high quality, optimize the language to be extremely attractive and professional in Arabic, "
        "and output the final polished content. Do not add any meta-commentary, just the final content."
    )
    response_agent3 = model.generate_content(prompt_agent3).text
    print("[Agent 3] تمت مراجعة المحتوى وتدقيقه وفق الشريعة والجودة.")

    # ----------------------------------------------------
    # Agent 4: Marketing & Monetization Loop (وكيل التسويق والنشر والربح)
    # ----------------------------------------------------
    # دمج المحتوى مع الرابط الربحي التلقائي الخاص بك
    final_post = (
        f"🤖 **منشور مؤتمت ومولد بالذكاء الاصطناعي يقدم قيمة حقيقية حلال:**\n\n"
        f"{response_agent3}\n\n"
        f"💼 للاستفادة الكاملة، الحصول على الأدوات المتقدمة أو طلب الاستشارات المخصصة، تفضل بزيارة رابطنا: {AFFILIATE_OR_STORE_LINK}\n"
        f"✨ الدخل من هذا المنشور يذهب لدعم تطوير الأنظمة المستقلة الحلال."
    )
    
    # النشر الآلي الفوري عبر التليجرام
    telegram_url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": final_post,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(telegram_url, json=payload)
    if response.status_code == 200:
        print("[Agent 4] تم نشر القيمة مدمجة برابط الربح بنجاح! حلقة مكتملة بنسبة 100%.")
    else:
        print(f"[-] خطأ في النشر: {response.text}")

if __name__ == "__main__":
    run_autonomous_loop()
