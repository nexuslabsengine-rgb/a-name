import os
import requests
import google.generativeai as genai

# إعداد مفاتيح التشغيل من متغيرات البيئة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_API_KEY = os.environ.get("BLOGGER_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
AFFILIATE_OR_STORE_LINK = os.environ.get("AFFILIATE_OR_STORE_LINK", "https://gumroad.com")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------- Agent 1: توليد الأفكار والقيم ----------
def agent_ideator():
    prompt = """أنت وكيل متخصص في تحليل السوق الرقمي.
أنتج فكرة واحدة محددة وقيمة لـ (منتج رقمي، أو حل مشكلة برمجية/خدمة، أو استشارة تقنية).
الشرط: أن تكون الفكرة مباحة شرعاً، تقدم قيمة حقيقية، وتحتاج حلولاً عمليّة (مثل: قالب كود، خطوات حل مشكلة، دليل تطبيقي).
قم بالرد بصيغة JSON تحتوي على:
{"title": "العنوان", "type": "product/service/consultation", "summary": "ملخص القيمة المقدمة"}"""
    
    response = model.generate_content(prompt)
    return response.text

# ---------- Agent 2: صناعة المحتوى والقيمة ----------
def agent_creator(idea_data):
    prompt = f"""أنت وكيل خبير في تنفيذ وبناء المنتجات والخدمات الرقمية.
بناءً على الفكرة التالية:
{idea_data}

قم بكتابة مقال أو دليل عملي شامل وممتع جداً يقدم قيمة حقيقية للجمهور.
- إذا كانت خدمة/استشارة: اشرح الخطوات بالتفصيل وأعطِ الأدوات والنصوص الإرشادية.
- إذا كان منتجاً: وفر الحل أو النموذج بشكل مكتمل.
- اجعل الأسلوب احترافياً، خبراً، وسهل القراءة مع استخدام عناوين وتنسيق Markdown."""
    
    response = model.generate_content(prompt)
    return response.text

# ---------- Agent 3: التدقيق الشرعي والجودة ----------
def agent_sharia_and_quality(content):
    prompt = f"""أنت وكيل تدقيق الجودة والالتزام بالمعايير الأخلاقية والشرعية الإسلامية.
راجع المحتوى التالي:
{content}

المهام:
1. تأكد من عدم وجود أي خداع، غرر، أو إيهام للربح السريع الكاذب.
2. تأكد من وجود قيمة حقيقية وفائدة للمستخدم.
3. قم بتحسين الصيغة، وتأكيد خلو المحتوى من أي محرمات أو توجيهات ضارة.
4. أعد كتابة النص النهائي المحسن فقط."""
    
    response = model.generate_content(prompt)
    return response.text

# ---------- Agent 4: التسويق والنشر التلقائي ----------
def agent_publisher(final_content):
    # إضافة رابط الربح الحلال في نهاية المحتوى
    monetized_content = f"{final_content}\n\n---\n💡 **للحصول على المزيد من المصادر والأدوات المتقدمة:** [{AFFILIATE_OR_STORE_LINK}]({AFFILIATE_OR_STORE_LINK})"
    
    # 1. النشر على Blogger (لجذب زوار البحث SEO)
    url_blogger = f"https://www.googleapis.com/urlshortener/v1/url" # مسار النشر لـ Blogger API
    blogger_post_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/?key={BLOGGER_API_KEY}"
    
    post_body = {
        "kind": "blogger#post",
        "title": final_content.split('\n')[0].replace('#', '').strip(),
        "content": monetized_content.replace('\n', '<br>')
    }
    
    try:
        requests.post(blogger_post_url, json=post_body)
        print("تم النشر على Blogger بنجاح.")
    except Exception as e:
        print(f"خطأ في نشر Blogger: {e}")

    # 2. النشر على Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": monetized_content[:4000],  # حد تليجرام للمسجات
        "parse_mode": "Markdown"
    }
    try:
        requests.post(telegram_url, json=payload)
        print("تم النشر على Telegram بنجاح.")
    except Exception as e:
        print(f"خطأ في نشر Telegram: {e}")

# ---------- التشغيل الذاتي للحلقة (The Loop) ----------
if __name__ == "__main__":
    print("بدء دورة الوكلاء المستقلة...")
    idea = agent_ideator()
    raw_content = agent_creator(idea)
    verified_content = agent_sharia_and_quality(raw_content)
    agent_publisher(verified_content)
    print("تمت الدورة بنجاح ودون أي تدخل بشري!")
