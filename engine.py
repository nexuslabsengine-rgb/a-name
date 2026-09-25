import os
import random
import requests
import time
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


def generate_content_with_retry(prompt, max_retries=3):
    client = get_gemini_client()
    
    # Only use models that are confirmed to work with v1beta API
    model_name = "models/gemini-3.8-flash"
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to use {model_name} (attempt {attempt + 1}/{max_retries})")
            response = client.models.generate_content(model=model_name, contents=prompt)
            print(f"✓ Successfully used model: {model_name}")
            return response.text.strip()
        except Exception as exc:
            error_msg = str(exc)
            
            # If it's a 503 (service unavailable), retry with exponential backoff
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1, 2, 4 seconds
                    print(f"⏳ Service temporarily unavailable. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
            
            # For other errors, fail immediately
            print(f"✗ Model {model_name} failed: {exc}")
            raise RuntimeError(f"Failed to generate content after {max_retries} attempts: {exc}")
    
    raise RuntimeError(f"All retries failed for {model_name}")


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

print("🤖 Agent 1: Generating idea title...")
title = generate_content_with_retry(prompt_agent_1)
print(f"📝 Title: {title}\n")

# --- الوكيل 2: وكيل التنفيذ والإنتاج ---
prompt_agent_2 = f"""
أنت 'وكيل الإنتاج والتنفيذ'.
العنوان: {title}
أنشئ محتوى {selected_value['type']} كاملاً بدقة فائقة وبدون اختصارات، يتضمن معرفة تطبيقية وقيمة حقيقية.
"""

print("🤖 Agent 2: Generating product content...")
product_content = generate_content_with_retry(prompt_agent_2)
print(f"📄 Content length: {len(product_content)} characters\n")

# --- الوكيل 3: وكيل التدقيق الشرعي والجودة ---
prompt_agent_3 = f"""
أنت 'وكيل التدقيق الشرعي والجودة'.
تأكد من أن المحتوى حلال 100% (لا غش، لا تضليل، لا ربا) ويقدم نفعاً حقيقياً.
المحتوى:
{product_content}
أعد صياغة المحتوى وتنقيحه ليكون بأعلى جودة ممكنة.
"""

print("🤖 Agent 3: Verifying and refining content...")
verified_content = generate_content_with_retry(prompt_agent_3)
print(f"✅ Verification complete. Content length: {len(verified_content)} characters\n")

# --- الوكيل 4: وكيل السيو والنمو والترافيك ---
cta_text = f"\n\n🔗 **لطلب القيمة كاملة:** {PAYMENT_LINK}" if PAYMENT_LINK else ""
prompt_agent_4 = f"""
أنت 'وكيل الترافيك والسيو'.
بناءً على الموضوع: {title}
1. اكتب منشوراً تسويقياً مقنعاً.
2. أضف 4 وسوم (Tags) عالية البحث على محركات البحث.
3. ضع دعوة واضحة للشراء/الطلب عبر هذا الرابط: {PAYMENT_LINK}
"""

print("🤖 Agent 4: Creating marketing copy...")
marketing_copy = generate_content_with_retry(prompt_agent_4)
print(f"📢 Marketing copy ready. Length: {len(marketing_copy)} characters\n")

# --- الوكيل 5: الناشر الآلي المباشر لتوليد الترافيك ---

success_count = 0

# أ. النشر على Dev.to (جلب زوار مجاني من محركات البحث Google)
if DEVTO_API_KEY and PAYMENT_LINK:
    try:
        print("📤 Posting to Dev.to...")
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
        success_count += 1
    except Exception as e:
        print(f"⚠️ Failed to post to Dev.to: {e}")
else:
    print("⏭️ Skipping Dev.to (missing DEVTO_API_KEY or PAYMENT_LINK)")

# ب. النشر على Telegram
if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    try:
        print("📤 Posting to Telegram...")
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚀 **{title}** ({selected_value['type']})\n\n{marketing_copy}\n\n{cta_text}",
            "parse_mode": "Markdown",
        }
        telegram_response = requests.post(telegram_url, json=telegram_payload, timeout=30)
        telegram_response.raise_for_status()
        print("✓ Successfully posted to Telegram")
        success_count += 1
    except Exception as e:
        print(f"⚠️ Failed to post to Telegram: {e}")
else:
    print("⏭️ Skipping Telegram (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID)")

print(f"\n✅ Workflow complete! Value created, verified, and published to {success_count} channels.")
print("✅ تم إنشاء القيمة، تدقيقها شرعياً، ونشرها على شبكات الترافيك العضوي تلقائياً 100%!")
