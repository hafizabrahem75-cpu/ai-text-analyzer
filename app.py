import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="منصة حافظ السراء", page_icon="🧠")

# إعداد المفتاح بشكل مباشر وآمن
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام الإصدار الأحدث من النموذج
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("تأكد من إعداد المفتاح في الـ Secrets")
    st.stop()

st.title("🧠 منصة حافظ السراء")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            st.write(str(e))
