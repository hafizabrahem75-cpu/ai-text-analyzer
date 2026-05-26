import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="ذكاء حافظ السراء الاصطناعي", page_icon="🧠", layout="centered")

st.title("🧠 منصة حافظ السراء للذكاء الاصطناعي")
st.write("مرحباً بك! أنا مساعدك الذكي الشامل، اسألني في أي شيء وسأجيبك فوراً وبشكل مباشر.")

# اطلب مفتاح الـ API من المستخدم بشكل آمن لكي يعمل عقل البرنامج
# (يمكنك الحصول عليه مجاناً من Google AI Studio)
gemini_key = st.sidebar.text_input("أدخل مفتاح Google API Key الخاص بك:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق السؤال السفلي
user_query = st.chat_input("اسألني عن أي شيء يدور في عقلك...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 جاري التفكير والكتابة...")
        
        if gemini_key:
            try:
                # تشغيل عقل جيميناي الحقيقي للإجابة المباشرة والتلقائية
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-pro')
                
                # إرسال السؤال مع توجيه صارم بالرد المباشر بالعربية
                full_prompt = f"أجب على السؤال التالي مباشرة بدون أي مقدمات ترحيبية وباللغة العربية الفصحى: {user_query}"
                response = model.generate_content(full_prompt)
                answer = response.text
            except Exception as e:
                answer = "حدث خطأ أثناء الاتصال بعقل الذكاء الاصطناعي، يرجى التأكد من صلاحية المفتاح."
        else:
            answer = "⚙️ فضلاً يا صديقي، لكي أتمكن من إجابتك تلقائياً وبذكاء كامل مثلي، قم بإنشاء مفتاح مجاني من (Google AI Studio) وضعه في الصندوق الجانبي ليعمل الموقع فوراً!"

        message_placeholder.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- الترتيب النظيف في أسفل الصفحة تماماً ---
st.markdown("<br><br><hr>", unsafe_allow_html=True)
with st.expander("ℹ️ معلومات المطور وحقوق الملكية"):
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>جميع الحقوق محفوظة © 2026</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center;'><a href='https://wa.me/967717245252' target='_blank' style='background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: block;'>💬 راسلنا عبر الواتساب</a></p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center;'><a href='https://www.facebook.com/share/1CgpiG9TYR/' target='_blank' style='background-color: #1877F2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: block;'>🔗 تابعنا على فيسبوك</a></p>", unsafe_allow_html=True)
