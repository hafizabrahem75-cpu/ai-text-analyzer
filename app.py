import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# 2. إعداد المفتاح والنموذج
try:
    # قراءة المفتاح من Streamlit Secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # استخدام نموذج مستقر ومتاح للجميع
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error("خطأ في المفتاح: تأكد من إعداد GOOGLE_API_KEY في الـ Secrets.")
    st.stop()

# 3. الواجهة
st.title("🧠 منصة حافظ السراء")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. صندوق الإدخال
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
            st.error("حدث خطأ أثناء الاتصال بالنموذج. تأكد من تفعيل خدمة Gemini API في حسابك.")
            st.write(f"تفاصيل الخطأ: {e}")
