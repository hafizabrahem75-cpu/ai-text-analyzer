import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء")

# التهيئة
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام النموذج الأكثر توافقاً حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في التهيئة: {e}")
    st.stop()

st.title("🧠 منصة حافظ السراء")

# عرض المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# الإدخال
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
            st.write(e)
