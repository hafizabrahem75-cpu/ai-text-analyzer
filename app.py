import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="ذكاء حافظ السراء الاصطناعي", page_icon="🧠", layout="centered")

# عنوان المنصة الرئيسي
st.title("🧠 منصة حافظ السراء للذكاء الاصطناعي")
st.write("اسألني في أي شيء، وسأجيبك فوراً وبشكل مباشر دون مقدمات.")

# محاولة الاتصال التلقائي بالمفتاح من السيرفر
try:
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة الخاص بالشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة المستمرة في منتصف الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق إدخال الأسئلة (أسفل الشاشة)
user_query = st.chat_input("اسألني عن أي شيء يدور في عقلك...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 جاري التفكير والكتابة...")
        
        if has_api:
            try:
                # إرسال الطلب ليعطي جواباً مباشراً دون أي عبارات ترحيبية
                full_prompt = f"أجب على السؤال التالي مباشرة باللغة العربية وبدون مقدمات أو جمل ترحيبية: {user_query}"
                response = model.generate_content(full_prompt)
                answer = response.text
            except Exception:
                answer = "عذراً يا صديقي، واجه المحرك ضغطاً مؤقتاً، يرجى المحاولة مرة أخرى."
        else:
            answer = "⚙️ النظام بانتظار ترتيب المفتاح السري داخل إعدادات السيرفر (Secrets) لتبدأ الإجابة تلقائياً."

        message_placeholder.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


# --- التعديل المطلوب: تذييل الصفحة المنسق (الأزرار والاسم علناً في الأسفل) ---
st.markdown("<br><br><hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)

# أزرار تواصل صغيرة ومتوسطة الحجم في سطر واحد وعلناً للمستخدمين
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 8px;">
        <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">💬 واتساب</a>
        <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">🔗 فيسبوك</a>
    </div>
    """, 
    unsafe_allow_html=True
)

# الاسم يظهر علناً للقراء بخط ناعم وصغير في قاع الصفحة تماماً
st.markdown("<p style='text-align: center; color: #777777; font-size: 12px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
