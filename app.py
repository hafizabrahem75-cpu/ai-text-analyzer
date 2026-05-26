import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# العنوان الرئيسي المنسق والمصغر على شاشات الجوال
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 14px;'>مساعدك الذكي: اسألني أي سؤال أو اطلب مني رسم وتوليد أي صورة فوراً!</p>", unsafe_allow_html=True)

# ربط النظام بالمفتاح السري تلقائياً من السيرفر
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة للحفاظ على انسيابية المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل في المنتصف بشكل متتابع
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# صندوق إدخال الأسئلة والأوامر في الأسفل
user_query = st.chat_input("اسألني عن أي شيء، أو اطلب صورة...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # تنظيف النص البرمجي للبحث عن التحيات أو الرسوم
        clean_query = user_query.strip()
        
        # 1. الرد المباشر الذكي على التحيات اليومية دون الحاجة للسيرفر الخارجي
        if clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك، كيف يمكنني مساعدتك اليوم؟"
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        elif clean_query in ["هاي", "هلو", "hello", "hi"]:
            answer = "أهلاً بك! اسألني عن أي شيء وسأجيبك فوراً."
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        # 2. معالجة طلبات الصور
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]):
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة فوراً...")
            try:
                encoded_prompt = urllib.parse.quote(clean_query)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الصورة التي طلبتها لـ: {user_query}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً مؤقتاً، يرجى إعادة المحاولة.")
                
        # 3. معالجة الأسئلة العامة عبر الذكاء الاصطناعي
        else:
            message_placeholder.markdown("🧠 جاري التفكير والكتابة...")
            if has_api:
                try:
                    full_prompt = f"أجب على السؤال التالي مباشرة باللغة العربية وبدون مقدمات أو جمل ترحيبية أو تكرار للسؤال: {clean_query}"
                    response = model.generate_content(full_prompt)
                    answer = response.text
                except Exception:
                    answer = "أنا جاهز للإجابة على كافة أسئلتك البرمجية والعلمية بدقة، يرجى إعادة كتابة السؤال."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})


# --- الترتيب الثابت والمستقر في الأسفل تماماً (تذييل الصفحة) ---
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

# اسم المطور ظاهر علناً للقراء بخط صغير وأنيق في نهاية الصفحة
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
