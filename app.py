import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الاحترافية وتثبيت التصميم كأنه تطبيق هاتف
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# حقن أكواد CSS المتقدمة لتغيير واجهة Streamlit التقليدية إلى واجهة تطبيق ذكي (تشبه التخطيط الهندسي)
st.markdown("""
    <style>
    /* إخفاء القوائم الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تنسيق الحاوية الرئيسية */
    .block-container {padding-top: 1.5rem; padding-bottom: 6rem;}
    
    /* تحسين شكل صندوق المدخلات ليكون منحنياً وعصرياً */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        background-color: #1a1a1a !important;
    }
    
    /* تنسيق الرسائل والأزرار */
    .stAudio {
        margin-top: 8px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# الواجهة العلوية الأنيقة والمصغرة للموبايل
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold; margin-bottom:0;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a2be2; font-size: 13px; font-weight: bold; margin-top:5px;'>💡 مساعدك الخارق: يدمج الصور مع النصوص، ويدعم الأوامر الصوتية بالكامل!</p>", unsafe_allow_html=True)
st.markdown("<hr style='border:0.5px solid #333; margin-top:10px; margin-bottom:20px;'>", unsafe_allow_html=True)

# ربط المفتاح السري بأحدث طراز رسمي خارق من جوجل
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة المستمرة للمحادثة وحفظ الصور لمنع مسحها عند إعادة التحميل
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# عرض المحادثات السابقة بشكل متناسق في منتصف الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# --- شريط الأدوات المتقدم (ميزة دمج لقطات الشاشة مع النص) ---
st.markdown("<p style='color: #aaa; font-size: 13px; margin-bottom: 2px;'>📸 1. أرفق لقطة الشاشة أو المشكلة من هنا أولاً (إذا وُجدت):</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="widget_uploader", label_visibility="collapsed")

if uploaded_file:
    st.session_state.current_image = Image.open(uploaded_file)
    st.image(st.session_state.current_image, caption="📸 تم تثبيت لقطة الشاشة بنجاح! الآن اكتب سؤالك عنها بالأسفل أو تحدث بالميكروفون.", width=250)

# --- ميزة زر الميكروفون السحري للهمس والكلام ---
st.markdown("<p style='color: #aaa; font-size: 13px; margin-bottom: 2px; margin-top:15px;'>🎙️ 2. إذا كنت لا تفضل الكتابة، اضغط على الميكروفون وتحدث ليتحول صوتك إلى نص تلقائياً:</p>", unsafe_allow_html=True)

# إضافة ميكروفون مدمج يعتمد على ميزة التعرف على الصوت الخاصة بالمتصفح (HTML5 Web Speech API)
text_from_speech = ""
click_mic = st.button("🎤 اضغط هنا للهمس والتحدث بالصوت")
if click_mic:
    st.markdown("""
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'ar-YE'; // ضبط اللهجة على توقيت اليمن والعربية
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        recognition.start();
        
        recognition.onresult = function(event) {
            var speechResult = event.results[0][0].transcript;
            // إرسال النص إلى حقل الإدخال
            const chatInput = parent.document.querySelector('textarea[aria-label="اكتب سؤالك هنا..."]');
            if (chatInput) {
                chatInput.value = speechResult;
                chatInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        </script>
    """, unsafe_allow_html=True)
    st.info("🎙️ جاري الاستماع لنبرة صوتك... تكلم الآن، وعندما تتوقف سيتحول كلامك إلى نص تلقائياً في صندوق الإدخال بالأسفل!")

# صندوق إدخال الأسئلة والأوامر الرئيسي (يدعم الكتابة أو استقبال النص المحول من الصوت)
user_query = st.chat_input("اكتب سؤالك هنا...")

if user_query or (st.session_state.current_image and not st.session_state.messages):
    # إذا لم يكتب المستخدم شيئاً ولكنه رفع صورة، نضع له أمراً تلقائياً للتحليل
    query_text = user_query if user_query else "حلل هذه الصورة بالكامل واستخرج المشاكل والأكواد التي بها كخبير محترف وجاوبني بدقة."
    
    with st.chat_message("user"):
        st.markdown(query_text)
        if st.session_state.current_image:
            st.image(st.session_state.current_image)
            
    st.session_state.messages.append({"role": "user", "content": query_text})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        clean_query = query_text.strip()
        
        # حساب توقيت اليمن برمجياً بشكل دقيق ومدمج
        utc_now = datetime.utcnow()
        yemen_now = utc_now + timedelta(hours=3)
        time_str = yemen_now.strftime("%I:%M %p")
        date_str = yemen_now.strftime("%Y-%m-%d")
        
        # 1. الرد الفوري الذكي على التحيات المباشرة لعدم التكرار
        if clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا بشمهندس حافظ، أنا منصتك الخارقة وجاهز لقراءة وتحليل لقطات الشاشة والصوتيات فوراً."
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        # 2. ميزة معرفة الوقت والساعة بدقة دون عجز
        elif any(keyword in clean_query for keyword in ["كم الساعه", "الوقت الان", "الساعه كم", "كم الوقت", "ساعه كم"]):
            answer = f"🕒 الوقت الآن في اليمن هو تمام الساعة: {time_str} \n📅 وتاريخ اليوم هو: {date_str}"
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        # 3. ميزة توليد الصور الفائقة والذكية
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]) and not st.session_state.current_image:
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة بدقة خارقة وتفاصيل كاملة...")
            try:
                enhanced_query = clean_query + " highly detailed, realistic, full background photorealistic"
                encoded_prompt = urllib.parse.quote(enhanced_query)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&private=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الرسمة الاحترافية التي طلبتها لـ: {query_text}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً، يرجى المحاولة مرة أخرى.")
                
        # 4. معالجة لقطات الشاشة المدمجة مع النصوص (الذكاء الخارق الشامل للبحوث والترجمة ومشاكل الأكواد)
        else:
            message_placeholder.markdown("🧠 جاري التفكير والتحليل الشامل كقدوتك Gemini...")
            if has_api:
                try:
                    # صياغة الأمر الموجه لعقل جوجل ليدمج الصورة والنص معاً ويدعم الترجمة والبحوث
                    system_prompt = f"التوقيت الحالي في اليمن هو {date_str} {time_str}. أجب مباشرة باللغة العربية وبدون مقدمات ترحيبية، وقدم حلاً قطعياً وشاملاً ومفصلاً ومصلحاً بناءً على النص والصورة المرفقة: {clean_query}"
                    
                    if st.session_state.current_image:
                        response = model.generate_content([system_prompt, st.session_state.current_image])
                    else:
                        response = model.generate_content(system_prompt)
                        
                    answer = response.text
                except Exception:
                    answer = "أنا جاهز ومستعد تماماً لمساعدتك في كافة البحوث، الترجمة، حل الأكواد وقراءة لقطات الشاشة المدمجة. يرجى إعادة إرسال الطلب بوضوح."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # تفريغ ذاكرة الكاش للصورة المرفوعة بعد اكتمال الحل بنجاح لاستقبال الصورة التالية
    st.session_state.current_image = None

# --- الترتيب الاحترافي الثابت في قاع الصفحة تماماً (التذييل الشامل) ---
st.markdown("<br><br><hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 10px;">
        <div style="color: #888888; font-size: 13px; font-weight: bold;">المطور: حافظ السراء © 2026</div>
        <div>
            <a href="https://wa.me/967717245252" target="_blank" style="background-color: #25D366; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 5px;">واتساب</a>
            <a href="https://www.facebook.com/share/1CgpiG9TYR/" target="_blank" style="background-color: #1877F2; color: white; padding: 5px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 12px;">فيسبوك</a>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
