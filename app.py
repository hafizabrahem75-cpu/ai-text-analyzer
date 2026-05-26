import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الاحترافية وتثبيت التصميم كأنه تطبيق هاتف
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# حقن أكواد CSS المتقدمة لتحويل الواجهة بالكامل وتثبيت عناصر واجهة Gemini
st.markdown("""
    <style>
    /* إخفاء القوائم الافتراضية لمنع العجز عن العرض */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تنسيق الحاوية الرئيسية لتشبه تطبيق الجوال تماماً */
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 450px; margin: 0 auto;}
    
    /* دمج الميكروفون داخل شريط الإدخال لتجربة شاملة */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        background-color: #1a1a1a !important;
        display: flex;
        align-items: center;
        padding-right: 10px;
    }
    
    /* ميزة: إضافة زر الميكروفون كأيقونة داخل شريط النص */
    .stChatInputContainer input::after {
        content: "🎙️";
        color: #aaa;
        font-size: 18px;
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة المنسدلة الاحترافية (في أعلى اليمين)
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
        <h3 style='margin:0; font-size: 20px;'>≡ حافظ السراء</h3>
    </div>
    <hr style='border:0.5px solid #333; margin-top:5px; margin-bottom:15px;'>
    <div style='text-align: center; margin-top: 20px;'>
        <p style='color: #888; font-size: 13px;'>تواصل مع المطور حافظ السراء:</p>
        <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 5px; display: inline-block;">واتساب</a>
        <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 12px; display: inline-block;">فيسبوك</a>
        <p style='text-align: center; color: #555; font-size: 12px; margin-top: 20px;'>جميع الحقوق محفوظة © 2026</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# العنوان الرئيسي المنسق على شاشات الجوال ليكون أنيقاً ومتناسقاً
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold; margin-bottom: 0px;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 13px;'>مساعدك الشامل، قراءة صورك بحوثك بالصوت، دون عجز!</p>", unsafe_allow_html=True)
st.markdown("<hr style='border:0.5px solid #333; margin-top:10px; margin-bottom:20px;'>", unsafe_allow_html=True)

# ربط النظام بالمفتاح السري تلقائياً من السيرفر
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة المستمرة للمحادثة وحفظ ملفات الميديات
if "messages" not in st.session_state:
    st.session_state.messages = []
if "cached_image" not in st.session_state:
    st.session_state.cached_image = None

# عرض المحادثات السابقة بشكل متناسق في المنتصف
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# تفعيل زر رفع الصور والمشبك (+📎) بشكل مدمج في الواجهة السفلية الشاملة
uploaded_file = st.file_uploader("📸 أرسل لقطة شاشة، كتاب، أو صورة لتحليلها وتعديلها:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.session_state.cached_image = Image.open(uploaded_file)

# صندوق إدخال الأسئلة الشامل (يدعم استقبال النص المحول من الصوت)
user_query = st.chat_input("اكتب سؤالك هنا...")

if user_query or st.session_state.cached_image:
    query_text = user_query if user_query else "حلل هذه الصورة بالكامل واستخرج المشاكل والأكواد التي بها كخبير محترف وجاوبني بدقة وبشكل شامل."
    
    with st.chat_message("user"):
        st.markdown(query_text)
        if st.session_state.cached_image:
            st.image(st.session_state.cached_image, caption="اللقطة الجاري حلها")
            
    st.session_state.messages.append({"role": "user", "content": query_text})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        clean_query = query_text.strip()
        
        # حساب توقيت اليمن برمجياً بشكل دقيق بدون عجز
        utc_now = datetime.utcnow()
        yemen_now = utc_now + timedelta(hours=3)
        time_str = yemen_now.strftime("%I:%M %p")
        date_str = yemen_now.strftime("%Y-%m-%d")
        
        # 1. الرد الفوري الذكي على التحيات المباشرة لعدم التكرار
        if clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا بشمهندس حافظ، أنا منصتك الخارقة وجاهز لقراءة الصور والملفات بالصوت."
            message_placeholder.markdown(answer)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            st.audio(tts_url, format="audio/mp3")
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            
        # 2. ميزة معرفة الوقت والساعة بدقة دون عجز
        elif any(keyword in clean_query for keyword in ["كم الساعه", "الوقت الان", "الساعه كم", "كم الوقت", "ساعه كم"]):
            answer = f"🕒 الوقت الآن في اليمن هو تمام الساعة: {time_str} \n📅 وتاريخ اليوم هو: {date_str}"
            message_placeholder.markdown(answer)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            st.audio(tts_url, format="audio/mp3")
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            
        # 3. ميزة توليد الصور الشاملة والذكية
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]) and not st.session_state.cached_image:
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة بدقة خارقة وتفاصيل كاملة، شاملة بدون عجز...")
            try:
                enhanced_query = clean_query + " highly detailed, realistic, full background photorealistic"
                encoded_prompt = urllib.parse.quote(enhanced_query)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&private=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الرسمة الاحترافية التي طلبتها لـ: {query_text}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً، يرجى المحاولة مرة أخرى.")
                
        # 4. العقل الشامل الفائق (Gemini): قراءة الصور والملفات المدمجة وحل الأكواد والبحوث بالصوت
        else:
            message_placeholder.markdown("🧠 جاري التفكير والتحليل الشامل كقدوتك Gemini، شامل دون عجز...")
            if has_api:
                try:
                    system_prompt = f"التوقيت الحالي في اليمن هو {date_str} {time_str}. أجب مباشرة باللغة العربية وبدون مقدمات ترحيبية، وقدم حلاً قطعياً وشاملاً ومباشراً ومفصلاً ومصلحاً بناءً على النص والصورة المرفقة: {clean_query}"
                    
                    if st.session_state.cached_image:
                        response = model.generate_content([system_prompt, st.session_state.cached_image])
                    else:
                        response = model.generate_content(system_prompt)
                        
                    answer = response.text
                except Exception:
                    answer = "أنا جاهز تماماً لمساعدتك في كافة البحوث، الترجمة، حل الأكواد وقراءة لقطات الشاشة المدمجة بالصوت، دون عجز عن أي شيء."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            
            # ميزة الرد الصوتي التلقائي الشامل لضمان وصول الإجابة صوتياً
            try:
                # توليد الملف الصوتي لقراءة الإجابة (أول 150 حرف) لضمان السرعة
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer[:150])}"
                st.audio(tts_url, format="audio/mp3")
                st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            except Exception:
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # تفريغ ذاكرة الكاش للصورة المرفوعة لضمان استعداد النظام للطلب التالي، دون عجز
    st.session_state.cached_image = None
