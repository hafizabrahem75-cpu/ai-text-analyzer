import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from datetime import datetime, timedelta
import base64
import io

# 1. إعدادات الصفحة الاحترافية لتطبيق الجوال
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# حقن أكواد CSS مخصصة لإخفاء كل زوائد Streamlit وتثبيت شريط الأدوات السفلي
st.markdown("""
    <style>
    /* إخفاء القوائم الافتراضية وهيدر وفوتير المتصفح */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stSidebarNav"] {display: none;}
    
    /* ضبط الحاوية الرئيسية لتبدو كتطبيق جوال نقي */
    .block-container {
        padding-top: 1rem; 
        padding-bottom: 7rem; 
        max-width: 480px; 
        margin: 0 auto;
    }
    
    /* تصميم الشريط السفلي العالمي الثابت (طبق الأصل من واجهة Gemini) */
    .gemini-input-bar {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 430px;
        background-color: #1e1e24;
        border-radius: 30px;
        padding: 8px 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        z-index: 9999;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية المنسدلة المخفية (تظهر عند سحب الشاشة أو الضغط على السهم)
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h3 style='color: white; margin-bottom: 5px;'>≡ حافظ السراء</h3>
            <p style='color: #888; font-size: 13px;'>منصة الذكاء الاصطناعي الشاملة</p>
            <hr style='border-color: #333;'>
            <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 6px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px; display: block; margin: 10px 0;">💬 تواصل عبر واتساب</a>
            <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 6px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px; display: block; margin: 10px 0;">🔗 تواصل عبر فيسبوك</a>
            <p style='color: #444; font-size: 11px; margin-top: 30px;'>جميع الحقوق محفوظة © 2026</p>
        </div>
    """, unsafe_allow_html=True)

# واجهة التطبيق العلوية النظيفة
st.markdown("<h3 style='text-align: center; color: white; font-size: 22px; font-weight: bold; margin-bottom:0;'>🧠 منصة حافظ السراء للذكاء الاصطناعي</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a2be2; font-size: 12px; margin-top:5px;'>المساعد الخارق: لقطات شاشة، دمج نصوص، وأوامر صوتية شاملة</p>", unsafe_allow_html=True)
st.markdown("<hr style='border:0.5px solid #222; margin-bottom:15px;'>", unsafe_allow_html=True)

# ربط الـ API بمفتاح جوجل الخارق
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# إدارة الذاكرة المستمرة للمحادثة لضمان عدم اختفاء البيانات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض صندوق المحادثة المتتابع في المنتصف
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# --- هندسة الواجهة السفلية العالمية (أزرار مدمجة في سطر واحد حقيقي) ---

# 1. زر رفع الملفات والمشابك (+) مخفي بشكل أنيق ومدمج فوق الشريط أو بداخلة برمجياً
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="hidden_upload", label_visibility="collapsed")

# الإدخال الصوتي والكتابي باستخدام مكونات ذكية مدمجة في سطر واحد
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    # ميكروفون مدمج يحول الصوت إلى نص عبر المتصفح فوراً دون عجز
    mic_clicked = st.button("🎙️", help="اضغط للتحدث بالصوت")
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
        st.toast("🎙️ جاري الاستماع لصوتك.. تحدث الآن!")

with col2:
    # صندوق النص الأساسي في نفس السطر
    user_text = st.text_input("", placeholder="اسأل Gemini...", label_visibility="collapsed")

with col3:
    # زر الإرسال السهمي المقابل
    submit_button = st.button("▲")

# معالجة الطلب في حال أرسل المستخدم نصاً أو رفع صورة
if submit_button and (user_text or uploaded_file):
    current_image = None
    query_text = user_text if user_text else "حلل هذه الصورة واشرح الإشكالية التي بها بالتفصيل."
    
    # عرض مدخلات المستخدم في المحادثة
    with st.chat_message("user"):
        st.markdown(query_text)
        if uploaded_file:
            current_image = Image.open(uploaded_file)
            st.image(current_image, caption="اللقطة المرفوعة")
            
    # حفظ في الذاكرة
    st.session_state.messages.append({"role": "user", "content": query_text, "image": current_image if uploaded_file else None})

    # معالجة رد الذكاء الاصطناعي (Gemini 1.5 Flash الخارق)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 جاري التفكير والتحليل الشامل...")
        
        if has_api:
            try:
                # حساب التوقيت في اليمن برمجياً ومدمجاً
                utc_now = datetime.utcnow()
                yemen_now = utc_now + timedelta(hours=3)
                time_str = yemen_now.strftime("%I:%M %p")
                date_str = yemen_now.strftime("%Y-%m-%d")
                
                system_prompt = f"أنت مساعد ذكي مدمج في منصة المهندس حافظ السراء. التوقيت الحالي: {date_str} {time_str}. حلل الصورة المرفقة والنص معاً بدقة متناهية وقدم حلاً برمجياً أو علمياً قاطعاً ومباشراً: {query_text}"
                
                if uploaded_file:
                    response = model.generate_content([system_prompt, current_image])
                else:
                    response = model.generate_content(system_prompt)
                    
                answer = response.text
            except Exception as e:
                answer = f"حدث خطأ أثناء الاتصال بالنظام، يرجى التحقق من المفتاح السري. التفاصيل: {str(e)}"
        else:
            answer = "⚙️ النظام بانتظار تفعيل المفتاح السري (GOOGLE_API_KEY) في إعدادات Secrets للبدء."
            
        message_placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
