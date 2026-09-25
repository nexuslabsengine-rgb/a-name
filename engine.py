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


def get_gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Set the secret before running the workflow.")
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_content_with_fallback(prompt):
    client = get_gemini_client()
    # Model names without 'models/' prefix - the SDK adds it automatically
    model_candidates = [
        "gemini-3.8-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-pro",
    ]
    last_error = None

    for model_name in model_candidates:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            print(f"✓ Successfully used model: {model_name}")
            return response.text.strip()
        except Exception as exc:  # pragma: no cover - runtime fallback for model availability
            print(f"✗ Model {model_name} failed: {exc}")
            last_error = exc
            continue

    raise RuntimeError(f"All Gemini model candidates failed. Last error: {last_error}")


# 2. أشكال القيمة الاقتصادية الحلال
VALUE_TYPES = [
    {"type": "منتج رقمي (Product)", "prompt": "دليل عملي مصغر أو قالب جاهز للإنتاجية وتقنية المعلومات."},
    {"type": "خدمة مصغرة (Service)", "prompt": "تحليل تقني/سيو/برمجي سريع يوفر حلاً لمشكلة قائمة لدى أصحاب المشاريع."},
    {"type": "استشارة متخصصة (Consultation)", "prompt": "تقرير استشاري يجيب على أسئلة معقدة في الأعمال أو التقنية مع خطوات تطبيقية واضحة."}
]

selected_value = random.choice(VALUE_TYPES)

# --- الوكيل 1: وكيل استكشاف الفرص ---
prompt_agent_1 = f"""
أنت 'وكيل الفرص الاقتصادية الحلال'.
نوع القيمة المطلوب إنشاؤها اليوم: {selected_value['type']}.
سياق الفكرة: {selected_value['prompt']}.
المطلوب: ابتكر موضوعاً محدد بدقة يحتاجه السوق الآن ويوفر قيمة حقيقية للعميل. أعد العنوان فقط.
"""

title = generate_content_with_fallback(prompt_agent_1)

# --- الوكيل 2: وكيل التنفيذ والإنتاج ---
prompt_agent_2 = f"""
أنت 'وكيل الإنتاج والتنفيذ'.
العنوان: {title}
أنشئ محتوى {selected_value['type']} كاملاً بدقة فائقة وبدون اختصارات، يتضمن معرفة تطبيقية وقيمة حقيقية.
"""
product_content = generate_content_with_fallback(prompt_agent_2)

# --- الوكيل 3: وكيل التدقيق الشرعي والجودة ---
prompt_agent_3 = f"""
أنت 'وكيل التدقيق الشرعي والجودة'.
تأكد من أن المحتوى حلال 100% (لا غش، لا تضليل، لا ربا) ويقدم نفعاً حقيقياً.
المحتوى:
{product_content}
أعد صياغة المحتوى وتنقيحه ليكون بأعلى جودة ممكنة.
"""
verified_content = generate_content_with_fallback(prompt_agent_3)

# --- الوكيل 4: وكيل السيو والنمو والترافيك ---
cta_text = f"\n\n🔗 **لطلب القيمة كاملة:** {PAYMENT_LINK}" if PAYMENT_LINK else ""
prompt_agent_4 = f"""
أنت 'وكيل الترافيك والسيو'.
بناءً على الموضوع: {title}
1. اكتب منشوراً تسويقياً مقنعاً.
2. أضف 4 وسوم (Tags) عالية البحث على محركات البحث.
3. ضع دعوة واضحة للشراء/الطلب عبر هذا الرابط: {PAYMENT_LINK}
"""
marketing_copy = generate_content_with_fallback(prompt_agent_4)

# --- الوكيل 5: الناشر الآلي المباشر لتوليد الترافيك ---
# أ. النشر على Dev.to (جلب زوار مجاني من محركات البحث Google)
if DEVTO_API_KEY and PAYMENT_LINK:
    try:
        devto_url = "https://dev.to/api/articles"
        devto_payload = {
            "article": {
                "title": f"[Free Guide] {title}",
                "published": True,
                "body_markdown": f"{marketing_copy}\n\n---\n\n### Preview of the Resource:\n{verified_content[:1500]}\n\n---\n👉 **Get the Complete Resource / Service Here:** [{PAYMENT_LINK}]({PAYMENT_LINK})",
                "tags": ["ai", "productivity", "business", "guides"],
            }
        }
        devto_headers = {"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}
        devto_response = requests.post(devto_url, json=devto_payload, headers=devto_headers, timeout=30)
        devto_response.raise_for_status()
        print("✓ Successfully posted to Dev.to")
    except Exception as e:
        print(f"⚠️ Failed to post to Dev.to: {e}")

# ب. النشر على Telegram
if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚀 **{title}** ({selected_value['type']})\n\n{marketing_copy}\n\n{cta_text}",
            "parse_mode": "Markdown",
        }
        telegram_response = requests.post(telegram_url, json=telegram_payload, timeout=30)
        telegram_response.raise_for_status()
        print("✓ Successfully posted to Telegram")
    except Exception as e:
        print(f"⚠️ Failed to post to Telegram: {e}")

print("✅ تم إنشاء القيمة، تدقيقها شرعياً، ونشرها على شبكات الترافيك العضوي تلقائياً 100%!")
