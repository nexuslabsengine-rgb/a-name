import os
import random
import requests
from google import genai

# 1. تهيئة المفاتيح من بيئة السيرفر
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PAYMENT_LINK = os.getenv("PAYMENT_LINK")

client = genai.Client(api_key=GEMINI_API_KEY)

# 2. مصفوفة القيم المتنوعة (حلال 100%)
VALUE_TYPES = [
    {
        "type": "منتج رقمي (Product)",
        "prompt": "دليل عملي مصغر أو قالب جاهز للاستخدام في مجالات الأعمال أو البرمجة أو الإنتاجية."
    },
    {
        "type": "خدمة مصغرة مؤتمتة (Service)",
        "prompt": "تحليل تقني/سيو/برمجي سريع يوفر حلاً لمشكلة قائمة لدى أصحاب المشاريع."
    },
    {
        "type": "استشارة متخصصة (Consultation)",
        "prompt": "تقرير استشاري يجيب على أسئلة معقدة في إدارة الأعمال أو التقنية مع خطوات تطبيقية."
    }
]

selected_value = random.choice(VALUE_TYPES)

# --- الوكيل 1: وكيل توليد الفرص ---
prompt_agent_1 = f"""
أنت 'وكيل الفرص الاقتصادية الحلال'.
نوع القيمة المطلوب إنشاؤها اليوم: {selected_value['type']}.
سياق الفكرة: {selected_value['prompt']}.

المطلوب: ابتكر عنواناً وموضوعاً محددين وبدقة عالية يحتاجهما السوق الآن فوراً وتوفر قيمة حقيقية للعميل.
اكتب عنوان الفكرة ونبذة من سطرين فقط.
"""

response_agent_1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_agent_1
)
idea = response_agent_1.text

# --- الوكيل 2: وكيل التنفيذ والإنتاج ---
prompt_agent_2 = f"""
أنت 'وكيل الإنتاج والتنفيذ'.
الفكرة المعتمدة:
{idea}

المطلوب: قم بإنشاء محتوى {selected_value['type']} كاملاً وبدقة فائقة بدون أي اختصارات.
يجب أن يحتوي على معرفة عملية، خطوات تطبيقية، أو نصائح قيمة يستفيد منها المشتري فوراً.
"""

response_agent_2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_agent_2
)
product_content = response_agent_2.text

# --- الوكيل 3: وكيل التدقيق الشرعي والجودة ---
prompt_agent_3 = f"""
أنت 'وكيل التدقيق الشرعي والجودة'.
راجع المحتوى التالي لتضمن الشروط التالية:
1. حلال 100% وفق الشريعة الإسلامية (لا غش، لا خداع، لا محتوى مضلل، لا ربا، لا ترويج لمحرمات).
2. يقدم قيمة حقيقية وصادقة للمستفيد.

المحتوى للمراجعة:
{product_content}

إذا كان المحتوى حلالاً وصالحاً، أعد صياغته وتنقيحه ليكون بأفضل صورة ممكنة للعميل.
"""

response_agent_3 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_agent_3
)
verified_content = response_agent_3.text

# --- الوكيل 4: وكيل التسويق والمبيعات ---
prompt_agent_4 = f"""
أنت 'وكيل التسويق المباشر'.
بناءً على المنتج/الخدمة التالية المعاينة منها:
{verified_content[:400]}...

قم بكتابة منشور تسويقي جذاب جداً وقصير للتليجرام يشرح القيمة المضافة بشكل مباشر، ويحتوي على دعوة للشراء/الطلب عبر هذا الرابط المباشر: {PAYMENT_LINK}
"""

response_agent_4 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_agent_4
)
sales_post = response_agent_4.text

# --- النشر الأوتوماتيكي عبر API ---
full_message = f"🚀 **عرض القيمة اليومي ({selected_value['type']})**\n\n{sales_post}\n\n---\n💡 **معاينة من القيمة المقدمة:**\n{verified_content[:300]}...\n\n🔗 **لطلب الخدمة/المنتج الكامل:** {PAYMENT_LINK}"

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": full_message,
    "parse_mode": "Markdown"
}

publish = requests.post(telegram_url, json=payload)

if publish.status_code == 200:
    print("✅ تم تشغيل حلقة الوكلاء بنجاح، وتدقيق العمل ونشره آلياً بنسبة 100%!")
else:
    print("❌ خطأ أثناء النشر:", publish.text)
