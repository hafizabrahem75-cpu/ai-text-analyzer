import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# 2. إعداد المفتاح والنموذج
try:
    # سيقرأ النظام المفتاح من Secrets تلقائياً
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # التعديل: استخدام هذا النموذج المحدث
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("خطأ: يرجى التأكد من إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# 3. الشريط الجانبي (القائمة المنسدلة والحسابات)
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.selectbox("حساباتي:", ["الحساب الرئيسي", "حساب العمل", "الحساب الشخصي"])
    st.markdown("---")
    st.write("منصة حافظ السراء - نسخة 2.0")

# 4. الواجهة الرئيسية
st.title("🧠 منصة حافظ السراء")

# أزرار تحكم إضافية (رفع ملفات + ميكروفون)
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🎤"):
        st.info("جاري تفعيل الميكروفون...")
with col2:
    # زر رفع الصور
    uploaded_file = st.file_uploader("رفع صورة", type=['png', 'jpg'], label_visibility="collapsed")

# 5. عرض المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. صندوق الإدخال
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
            st.error("حدث خطأ في الاتصال. تأكد من تفعيل Gemini API في حسابك على Google AI Studio.")
            st.write(f"تفاصيل الخطأ: {e}")
