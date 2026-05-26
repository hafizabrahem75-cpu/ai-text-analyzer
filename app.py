import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# 2. التهيئة باستخدام المفتاح السري المضمون
try:
    # سيقرأ النظام المفتاح من Secrets تلقائياً
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # التعديل هنا: استخدام نموذج gemini-pro لضمان الاستقرار
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("خطأ في الاتصال: تأكد من ضبط الـ GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# 3. واجهة المستخدم
st.title("🧠 منصة حافظ السراء")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. صندوق الإدخال (التصميم المستقر)
if prompt := st.chat_input("اسأل Gemini..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد المساعد
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء التوليد: {e}")
