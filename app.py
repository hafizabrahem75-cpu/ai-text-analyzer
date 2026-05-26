import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الاحترافية لتطبيق الجوال
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# حقن أكواد CSS ذكية لدمج زر الرفع والميكروفون داخل شريط الإدخال في سطر واحد حقيقي
st.markdown("""
    <style>
    /* إخفاء القوائم الافتراضية والزوائد الهيكلية لشاشة نقية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ضبط الحاوية الرئيسية لتناسب شاشات الجوال */
    .block-container {
        padding-top: 1rem; 
        padding-bottom: 6rem; 
        max-width: 480px; 
        margin: 0 auto;
    }
    
    /* هندسة السطر الواحد: تثبيت زر رفع الملفات والميكروفون في يسار شريط الإدخال */
    div[data-testid="stSidebarNav"] {display: none;}
    
    /* ضبط محاذاة شريط أدوات مدمج سفلي */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* تحسين مظهر أزرار السطر الواحد الإضافية */
    .floating-tools {
        position: fixed;
        bottom: 26px;
        left: calc(50% - 190px);
        display: flex;
        gap: 5px;
        z-index: 999999;
    }
    @media (max-width: 480px) {
        .floating-tools {
            left: 25px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية المخفية (تضم الاسم ووسائل التواصل)
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h3 style='color: white; margin-bottom: 5px;'>≡ حافظ السراء</h3>
            <p style='color: #888; font-size: 13px;'>منصة الذكاء الاصطناعي الشاملة</p>
            <hr style='border-color: #333;'>
            <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 6px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px; display: block; margin: 10px 0; text-align: center;">💬 تواصل عبر واتساب</a>
            <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 6px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px; display: block; margin: 10px 0; text-align: center;">🔗 تواصل عبر فيسبوك</a>
            <p style='color: #444; font-size: 11px; margin-top: 40px;'>جميع الحقوق محفوظة © 2026</p>
        </div>
    """, unsafe_allow_html=True)

# واجهة التطبيق العلوية النظيفة والأنيقة
st.markdown("<h3 style='text-align: center; color: white; font-size: 22px; font-weight: bold; margin-bottom:0;'>🧠 منصة حافظ السراء للذكاء الاصطناعي</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a2be2; font-size: 12px; margin-top:5px; font-weight: bold;'>المساعد الخارق: لقطات شاشة، نصوص، وأوامر صوتية في سطر واحد</p>", unsafe_allow_html=True)
st.markdown("<hr style='border:0.5px solid #222; margin-bottom:15px;'>", unsafe_allow_html=True)

# تفعيل والاتصال بمفتاح جوجل برمجياً ونقياً
has_api = False
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    if api_key and "ضع_مفتاحك" not in api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            has_api = True
        except Exception:
            pass

# إدارة ذاكرة الشات المستمرة لضمان عدم اختفاء البيانات عند التحديث
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة المتتابعة بشكل متناسق في المنتصف
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"] is not None:
            st.image(message["image"])

# --- هندسة وتصميم أزرار السطر الواحد المدمجة ---
# نضع زر رفع الملفات والميكروفون ليكونوا عائمين بشكل مدمج فوق يسار صندوق الإدخال تماماً
st.markdown('<div class="floating-tools">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="bar_upload", label_visibility="collapsed")
mic_clicked = st.button("🎙️", key="bar_mic", help="تحدث بالصوت")
st.markdown('</div>', unsafe_allow_html=True)

# تشغيل الميكروفون لتحويل الصوت إلى نص برمجياً فور الضغط عليه
if mic_clicked:
    st.markdown("""
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'ar-YE';
        recognition.start();
        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            var inputField = parent.document.querySelector('textarea[aria-label="اسأل Gemini..."]');
            if(inputField) {
                inputField.value = text;
                inputField.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        </script>
    """, unsafe_allow_html=True)
    st.toast("🎙️ جاري الاستماع لصوتك الآن...")

# صندوق الإدخال الذكي الموحد في الأسفل (السطر الموحد الفعلي)
user_text = st.chat_input("اسأل Gemini...")

# معالجة طلب الإرسال الموحد للنصوص واللقطات المرفوعة معاُ
if user_text:
    query_text = user_text
    current_img = None
    
    with st.chat_message("user"):
        st.markdown(query_text)
        if uploaded_file:
            current_img = Image.open(uploaded_file)
            st.image(current_img, caption="اللقطة المرفوعة")
            
    st.session_state.messages.append({"role": "user", "content": query_text, "image": current_img})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 جاري التفكير والتحليل الشامل...")
        
        if has_api:
            try:
                # ضبط التوقيت لليمن
                utc_now = datetime.utcnow()
                yemen_now = utc_now + timedelta(hours=3)
                time_str = yemen_now.strftime("%I:%M %p")
                date_str = yemen_now.strftime("%Y-%m-%d")
                
                system_prompt = f"أنت مساعد ذكي مدمج في منصة المهندس حافظ السراء. التوقيت الحالي في اليمن: {date_str} {time_str}. أجب بدقة واحترافية مباشرة باللغة العربية: {query_text}"
                
                if uploaded_file:
                    response = model.generate_content([system_prompt, current_img])
                else:
                    response = model.generate_content(system_prompt)
                
                answer = response.text
            except Exception as e:
                answer = f"⚠️ حدث خطأ أثناء الاتصال بالنظام: {str(e)}"
        else:
            answer = "⚙️ النظام بانتظار تفعيل وإصلاح كود الـ API الحقيقي في إعدادات Secrets للبدء فوراً."
            
        message_placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
