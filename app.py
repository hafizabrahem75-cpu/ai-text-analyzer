import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# إعداد المفتاح السري
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("خطأ: يرجى التأكد من وضع GOOGLE_API_KEY صحيحاً في الـ Secrets.")
    st.stop()

st.title("🧠 منصة حافظ السراء")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق الإدخال (الطريقة الوحيدة المستقرة)
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
            st.error(f"خطأ في الاتصال بـ Gemini: {e}")
