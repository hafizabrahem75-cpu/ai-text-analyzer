
import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# الواجهة الرئيسية المنسقة في الأعلى
st.title("🧠 منصة حافظ السراء للذكاء الاصطناعي")
st.write("مرحباً بك في منصتك الذكية الشاملة. اسألني في أي شيء، وسأجيبك فوراً وبشكل مباشر دون مقدمات.")

# ربط النظام بالمفتاح السري تلقائياً من السيرفر وتشغيل أحدث نموذج
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام النموذج الأحدث والأقوى والأسرع
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة للحفاظ على انسيابية المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل في المنتصف
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق إدخال الأسئلة والأوامر
user_query = st.chat_input("اسألني عن أي شيء يدور في عقلك...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 جاري التفكير والكتابة الفورية...")
        
        if has_api:
            try:
                # توجيه صارم للحصول على إجابة ذكية ومباشرة فوراً
                full_prompt = f"أجب على السؤال التالي مباشرة باللغة العربية وبدون مقدمات أو جمل ترحيبية: {user_query}"
                response = model.generate_content(full_prompt)
                answer = response.text
            except Exception:
                answer = "عذراً يا صديقي، واجه النظام ضغطاً مؤقتاً، يرجى إعادة إرسال السؤال."
        else:
            answer = "⚙️ النظام بانتظار لصق المفتاح السري داخل إعدادات السيرفر (Secrets) لتبدأ الإجابة تلقائياً."

        message_placeholder.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


# --- الترتيب الاحترافي النهائي: معلومات المطور ثابتة ومستقرة في الأسفل تماماً ---
st.markdown("<br><br><br><br><hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)

# أزرار تواصل علنية بحجم متوسط وأنيق في سطر واحد
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 5px;">
        <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 6px 15px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">💬 واتساب</a>
        <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 6px 15px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px; margin: 4px; display: inline-block;">🔗 فيسبوك</a>
    </div>
    """, 
    unsafe_allow_html=True
)

# اسم المطور ظاهر علناً للقراء بخط صغير وأنيق في نهاية الصفحة
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
