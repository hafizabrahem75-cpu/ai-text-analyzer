import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# إعداد المفتاح والنموذج
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام هذا النموذج الأكثر استقراراً في أغلب الحسابات
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("خطأ في المفتاح، تأكد من الـ Secrets.")
    st.stop()

# 1. الشريط الجانبي (القائمة المنسدلة والحسابات)
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.selectbox("حساباتي:", ["الحساب الرئيسي", "حساب العمل", "الحساب الشخصي"])
    st.markdown("---")
    st.write("منصة حافظ السراء - نسخة 2.0")

# 2. الواجهة الرئيسية
st.title("🧠 منصة حافظ السراء")

# أزرار تحكم إضافية (رفع ملفات + ميكروفون)
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🎤"):
        st.write("الميكروفون مفعل...")
with col2:
    uploaded_file = st.file_uploader("رفع صورة", type=['png', 'jpg'], label_visibility="collapsed")

# 3. عرض المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            # دمج الملف المرفوع إذا وجد
            content_to_send = prompt
            response = model.generate_content(content_to_send)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ: {e}")
