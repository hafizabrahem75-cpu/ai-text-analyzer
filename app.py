import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# 2. إعداد الـ API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ في الـ API Key: تأكد من وضعه بشكل صحيح في الـ Secrets بدون نصوص عربية.")
    st.stop()

# 3. واجهة المحادثة
st.title("🧠 منصة حافظ السراء")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. شريط الإدخال
if prompt := st.chat_input("اسأل Gemini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
