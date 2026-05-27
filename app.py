import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="منصة حافظ السراء")

try:
    # إعداد المفتاح
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # محاولة استخدام الإصدار الأحدث
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ في الاتصال، حاول لاحقاً.")
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
            st.error("تعذر الوصول للنموذج. جرب نموذجاً آخر.")
            st.write(f"خطأ تقني: {e}")
