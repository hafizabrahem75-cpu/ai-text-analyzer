import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة حافظ السراء", layout="centered")

# 2. إعداد المفتاح والنموذج
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # التغيير هنا: استخدام نموذج gemini-1.0-pro لضمان توافقه مع حسابك
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error("خطأ في إعداد المفتاح.")
    st.stop()

# 3. الشريط الجانبي
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.selectbox("حساباتي:", ["الحساب الرئيسي", "حساب العمل", "الحساب الشخصي"])
    st.markdown("---")
    st.write("منصة حافظ السراء - نسخة 2.0")

# 4. الواجهة الرئيسية
st.title("🧠 منصة حافظ السراء")

# أزرار تحكم
col1, col2 = st.columns([1, 5])
with col1:
    st.button("🎤")
with col2:
    st.file_uploader("رفع صورة", type=['png', 'jpg'], label_visibility="collapsed")

# 5. عرض المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. صندوق الإدخال
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
            st.error("خطأ: تأكد من تفعيل خدمة Gemini API في حسابك على Google AI Studio.")
            st.write(f"التفاصيل: {e}")
