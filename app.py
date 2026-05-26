import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء")

# إعداد المفتاح والنموذج
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # التغيير الجوهري هنا: نستخدم gemini-pro
    model = genai.GenerativeModel(gemini-1.5-flash-latest')
except Exception as e:
    st.error("خطأ في المفتاح.")
    st.stop()

st.title("🧠 منصة حافظ السراء")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
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
            
