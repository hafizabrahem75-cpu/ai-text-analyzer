import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="منصة حافظ السراء", page_icon="🧠")

# 2. إعداد الاتصال بـ Gemini
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام النموذج الأكثر توافقاً حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")
    st.stop()

# 3. الواجهة الأساسية
st.title("🧠 منصة حافظ السراء")

# ذاكرة المحادثة (لحفظ الرسائل)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. صندوق الإدخال (المحادثة)
if prompt := st.chat_input("اسأل Gemini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الإجابة
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("تعذر الاتصال بـ Gemini. يرجى التأكد من تفعيل API Key في Google AI Studio.")
            st.write(f"تفاصيل الخطأ التقني: {e}")
