import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء")

# 2. إعداد الاتصال
try:
    # التأكد من وجود المفتاح
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # محاولة الاتصال بنموذج gemini-pro (النموذج الأكثر استقراراً)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("خطأ في التهيئة. تأكد من إعداد المفتاح في الـ Secrets.")
    st.stop()

st.title("🧠 منصة حافظ السراء")

# 3. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الإدخال
if prompt := st.chat_input("اسأل Gemini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هنا التغيير: نستخدم generate_content المباشر
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("تعذر الاتصال بـ Gemini. هذا الخطأ يعني أن المفتاح لا يملك صلاحية الوصول للنموذج.")
            st.write(f"التفاصيل: {e}")
