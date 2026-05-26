import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="ذكاء حافظ السراء الاصطناعي", page_icon="🧠", layout="centered")

st.title("🧠 منصة حافظ السراء للذكاء الاصطناعي")
st.write("اسألني في أي شيء، وسأجيبك فوراً وبشكل مباشر دون مقدمات.")

# جلب المفتاح تلقائياً من إعدادات السيرفر المخفية
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    has_api = True
except Exception:
    has_api = False

# الذاكرة لتخزين المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة في منتصف الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق السؤال السفلي
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
                full_prompt = f"أجب على السؤال التالي مباشرة باللغة العربية الفصحى وبدون أي عبارات ترحيبية أو مقدمات: {user_query}"
                response = model.generate_content(full_prompt)
                answer = response.text
            except Exception:
                answer = "عذراً، واجه السيرفر مشكلة أثناء معالجة النص، يرجى المحاولة مرة أخرى."
        else:
            answer = "⚙️ التطبيق بانتظار تفعيل مفتاح الـ API من إعدادات السيرفر (Secrets)."

        message_placeholder.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


# --- التعديل الجديد: أزرار تواصل متوسطة واسمك بخط صغير في الأسفل تماماً ---
st.markdown("<br><br><hr style='border:0.5px solid #333;'>", unsafe_allow_html=True)

# الأزرار في سطر واحد وبحجم متوسط وأنيق
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 10px;">
        <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 6px 14px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px; margin: 5px; display: inline-block;">💬 واتساب</a>
        <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 6px 14px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px; margin: 5px; display: inline-block;">🔗 فيسبوك</a>
    </div>
    """, 
    unsafe_allow_html=True
)

# اسمك بخط صغير جداً وواضح للقراءة
st.markdown("<p style='text-align: center; color: #888888; font-size: 12px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
