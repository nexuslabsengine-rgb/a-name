import os
import random
import requests
from google import genai

# 1. جلب المفاتيح من بيئة السيرفر
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
PAYMENT_LINK = os.getenv("PAYMENT_LINK")

client = genai.Client(api_key=GEMINI_API_KEY)

# 2. أشكال القيمة الاقتصادية الحلال
VALUE_TYPES = [
    {"type": "منتج رقمي (Product)", "prompt": "دليل عملي مصغر أو قالب جاهز للإنتاجية وتقنية المعلومات."},
    {"type": "خدمة مصغرة (Service)", "prompt": "تحليل تقني/سيو/برمجي سريع يوفر حلاً لمشكلة قائمة لدى أصحاب المشاريع."},
    {"type": "استشارة متخصصة (Consultation)", "prompt": "تقرير استشاري يجيب على أسئلة معقدة في الأعمال أو التقنية مع خطوات تطبيقية."}
]

selected_value = random.choice(VALUE_TYPES)

# --- الوكيل 1: وكيل استكشاف الفرص ---
prompt_agent_1 = f"""
أنت 'وكيل الفرص الاقتصادية الحلال'.
نوع القيمة المطلوب إنشاؤها اليوم: {selected_value['type']}.
سياق الفكرة: {selected_value['prompt']}.
المطلوب: ابتكر موضوعاً محدد بدقة يحتاجه السوق الآن ويوفر قيمة حقيقية للعميل. أعد العنوان فقط.
"""
response_1 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_agent_1)
title = response_1.text.strip()

# --- الوكيل 2: وكيل التنفيذ والإنتاج ---
prompt_agent_2 = f"""
أنت 'وكيل الإنتاج والتنفيذ'.
العنوان: {title}
أنشئ محتوى {selected_value['type']} كاملاً بدقة فائقة وبدون اختصارات، يتضمن معرفة تطبيقية وقيمة حقيقية.
"""
response_2 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_agent_2)
product_content = response_2.text

# --- الوكيل 3: وكيل التدقيق الشرعي والجودة ---
prompt_agent_3 = f"""
أنت 'وكيل التدقيق الشرعي والجودة'.
تأكد من أن المحتوى حلال 100% (لا غش، لا تضليل، لا ربا) ويقدم نفعاً حقيقياً.
المحتوى:
{product_content}
أعد صياغة المحتوى وتنقيحه ليكون بأعلى جودة ممكنة.
"""
response_3 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_agent_3)
verified_content = response_3.text

# --- الوكيل 4: وكيل السيو والنمو والترافيك ---
prompt_agent_4 = f"""
أنت 'وكيل الترافيك والسيو'.
بناءً على الموضوع: {title}
1. اكتب منشوراً تسويقياً مقنعاً.
2. أضف 4 وسوم (Tags) عالية البحث على محركات البحث.
3. ضع دعوة واضحة للشراء/الطلب عبر هذا الرابط: {PAYMENT_LINK}
"""
response_4 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_agent_4)
marketing_copy = response_4.text

# --- الوكيل 5: الناشر الآلي المباشر لتوليد الترافيك ---

# أ. النشر على Dev.to (جلب زوار مجاني من محركات البحث Google)
devto_url = "https://dev.to/api/articles"
devto_payload = {
    "article": {
        "title": f"[Free Guide] {title}",
        "published": True,
        "body_markdown": f"{marketing_copy}\n\n---\n\n### Preview of the Resource:\n{verified_content[:1500]}\n\n---\n👉 **Get the Complete Resource / Service Here:** [{PAYMENT_LINK}]({PAYMENT_LINK})",
        "tags": ["ai", "productivity", "business", "guides"]
    }
}
devto_headers = {"api-key": DEVTO_API_KEY, "Content-Type": "json"}
requests.post(devto_url, json=devto_payload, headers={"api-key": DEVTO_API_KEY})

# ب. النشر على Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
telegram_payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": f"🚀 **{title}** ({selected_value['type']})\n\n{marketing_copy}\n\n🔗 **لطلب القيمة كاملة:** {PAYMENT_LINK}",
    "parse_mode": "Markdown"
}
requests.post(telegram_url, json=telegram_payload)

print("✅ تم إنشاء القيمة، تدقيقها شرعياً، ونشرها على شبكات الترافيك العضوي تلقائياً 100%!")
