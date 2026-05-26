import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# تنسيق واجهة العرض العلوية (تصغير خط العنوان ليكون أنيقاً ومتناسقاً على الموبايل)
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 14px;'>مساعدك الخارق: اسألني، أرسل لي صوراً ولقطات شاشة لتحليلها، أو اطلب توليد رسومات فوراً!</p>", unsafe_allow_html=True)

# ربط النظام بالمفتاح السري وتفعيل أحدث وأقوى نموذج من جوجل Gemini 2.5
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام النموذج العملاق الأحدث الداعم للنصوص والصور معاً
        model = genai.GenerativeModel('gemini-2.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة المستمرة للمحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة في منتصف الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# --- التعديل الجوهري: إضافة زر لرفع الصور ولقطات الشاشة للموقع ---
uploaded_file = st.file_uploader("📸 أرسل لقطة شاشة، كتاب، بحث، أو صورة لتعديلها وحلها:", type=["png", "jpg", "jpeg"])

# صندوق إدخال الأسئلة والأوامر في الأسفل
user_query = st.chat_input("اسألني عن أي شيء، أو اطلب صورة...")

if user_query or uploaded_file:
    # تحديد النص المرسل
    query_text = user_query if user_query else "حلل هذه الصورة واشرحها بالتفصيل"
    
    with st.chat_message("user"):
        st.markdown(query_text)
        if uploaded_file:
            st.image(uploaded_file, caption="اللقطة المرفوعة")
            
    # حفظ رسالة المستخدم في الذاكرة
    st.session_state.messages.append({"role": "user", "content": query_text})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        clean_query = query_text.strip()
        
        # 1. الرد الفوري الذكي على التحيات المباشرة
        if clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا صديقي، أنا تحت أمرك جاهز لحل المشاكل، البحوث، وقراءة الصور فوراً."
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        elif clean_query in ["هاي", "هلو", "hello", "hi"]:
            answer = "أهلاً بك! أنا منصتك الذكية الخارقة، اسألني في أي شيء أو ارفع لي ملفاتك وسأجيبك فوراً."
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        # 2. ميزة توليد الصور الفائقة عبر الأوامر النصية
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]) and not uploaded_file:
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة بدقة احترافية كاملة...")
            try:
                encoded_prompt = urllib.parse.quote(clean_query)
                # استخدام سيرفر توليد صور عالي الجودة ومحدث
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&private=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الصورة الاحترافية التي صممتها لك لـ: {query_text}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً، يرجى المحاولة مرة أخرى.")
                
        # 3. العقل الخارق (Gemini 2.5): معالجة النصوص، البحوث، الترجمة، وقراءة لقطات الشاشة!
        else:
            message_placeholder.markdown("🧠 جاري التفكير والتحليل العميق مثل Gemini...")
            if has_api:
                try:
                    # التوجيه الصارم لتقديم إجابة فورية ومباشرة بدون لف ودوران
                    system_prompt = f"أجب مباشرة باللغة العربية وبدون مقدمات ترحيبية أو تكرار للسؤال: {clean_query}"
                    
                    if uploaded_file:
                        # فتح الصورة وتهيئتها للذكاء الاصطناعي ليراها ويحللها كالعين البشرية
                        img = Image.open(uploaded_file)
                        response = model.generate_content([system_prompt, img])
                    else:
                        response = model.generate_content(system_prompt)
                        
                    answer = response.text
                except Exception as e:
                    answer = "أنا مبرمج ومستعد لمساعدتك في كافة البحوث، الترجمة، والأكواد. يرجى إعادة إرسال الطلب بوضوح."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# --- الترتيب الاحترافي الثابت والمستقر في الأسفل تماماً (تذييل الصفحة) ---
st.markdown("<br><br><hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)

# أزرار تواصل علنية بحجم متوسط وأنيق في سطر واحد
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 5px;">
        <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 6px 15px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">💬 واتساب</a>
        <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 6px 15px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">🔗 فيسبوك</a>
    </div>
    """, 
    unsafe_allow_html=True
)

# اسم المطور ظاهر علناً للقراء بخط صغير وأنيق في قاع الصفحة تماماً
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)

