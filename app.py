import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# إعداد المفتاح والنموذج
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # هذا هو النموذج الذي نستخدمه الآن في الكود
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ في إعداد المفتاح.")
    st.stop()

# الشريط الجانبي
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.selectbox("حساباتي:", ["الحساب الرئيسي", "حساب العمل", "الحساب الشخصي"])
    st.markdown("---")
    st.write("منصة حافظ السراء - نسخة 2.0")

# الواجهة الرئيسية
st.title("🧠 منصة حافظ السراء")

# أزرار تحكم
col1, col2 = st.columns([1, 5])
with col1:
    st.button("🎤")
with col2:
    st.file_uploader("رفع صورة", type=['png', 'jpg'], label_visibility="collapsed")

# عرض المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق الإدخال
if prompt := st.chat_input("اسأل Gemini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("حدث خطأ في الاتصال.")
            st.write(f"التفاصيل: {e}")
