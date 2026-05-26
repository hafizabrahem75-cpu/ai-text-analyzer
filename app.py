import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from datetime import datetime
import pytz  # لضبط توقيت اليمن بدقة
import base64

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# تنسيق واجهة العرض العلوية (تصغير خط العنوان ليكون أنيقاً ومتناسقاً على الموبايل)
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 14px;'>مساعدك الخارق: اسألني، تحدث معي، أرسل صوراً ولقطات شاشة لتحليلها، أو توليد رسومات فوراً!</p>", unsafe_allow_html=True)

# ربط النظام بالمفتاح السري وتفعيل أحدث وأقوى نموذج من جوجل Gemini 2.5
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة المستمرة للمحادثة وحفظ الملفات
if "messages" not in st.session_state:
    st.session_state.messages = []
if "saved_image" not in st.session_state:
    st.session_state.saved_image = None

# عرض الرسائل السابقة في منتصف الشاشة مع الحفاظ على ملفات الصوت والصور
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio_html" in message:
            st.markdown(message["audio_html"], unsafe_allow_html=True)

# --- التعديل الجوهري الأول: حفظ الصورة المرفوعة في الذاكرة لتجنب المسح ---
uploaded_file = st.file_uploader("📸 أرسل لقطة شاشة، كتاب، بحث، أو صورة لتعديلها وحلها:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.session_state.saved_image = Image.open(uploaded_file)
    st.image(st.session_state.saved_image, caption="📸 الصورة نشطة ومحفوظة الآن في ذاكرة النظام لدراستها أو التعديل عليها")

# صندوق إدخال الأسئلة والأوامر في الأسفل
user_query = st.chat_input("اسألني عن أي شيء، أو اطلب صورة...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
            
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        clean_query = user_query.strip()
        
        # التعديل الجوهري الثاني: الإجابة الذكية على الوقت والتاريخ بشكل حي وفوري لليمن
        if any(k in clean_query for k in ["الكم الساعه", "كم الساعه", "الوقت الان", "تاريخ اليوم", "كم الوقت"]):
            yemen_tz = pytz.timezone('Asia/Aden')
            now_yemen = datetime.now(yemen_tz)
            time_str = now_yemen.strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")
            date_str = now_yemen.strftime("%Y-%m-%d")
            answer = f"🕒 الوقت الحالي في اليمن هو: {time_str} \n📅 تاريخ اليوم هو: {date_str}."
            message_placeholder.markdown(answer)
            
            # ميزة الصوت المدمجة تلقائياً للرد
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            audio_html = f'<audio src="{tts_url}" autoplay controls style="width:100%; height:30px; margin-top:10px;"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio_html": audio_html})

        # 1. الرد الفوري الذكي على التحيات المباشرة
        elif clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا مهندس حافظ، أنا تحت أمرك جاهز لحل المشاكل والبحوث وقراءة لقطات الشاشة فوراً."
            message_placeholder.markdown(answer)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            audio_html = f'<audio src="{tts_url}" autoplay controls style="width:100%; height:30px; margin-top:10px;"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio_html": audio_html})
            
        # 2. ميزة توليد الصور الفائقة عبر الأوامر النصية
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]) and not st.session_state.saved_image:
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة بدقة احترافية كاملة...")
            try:
                encoded_prompt = urllib.parse.quote(clean_query)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&private=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الصورة الاحترافية التي صممتها لك لـ: {user_query}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً، يرجى المحاولة مرة أخرى.")
                
        # 3. العقل الخارق الداعم للنصوص والصور المحفوظة والبحوث والترجمة والصوت
        else:
            message_placeholder.markdown("🧠 جاري التفكير والتحليل العميق مثل Gemini...")
            if has_api:
                try:
                    system_prompt = f"أجب مباشرة وبخط واضح باللغة العربية وبدون مقدمات ترحيبية أو تكرار للسؤال: {clean_query}"
                    
                    # إذا كانت هناك صورة محفوظة في الذاكرة، يتم إرسالها للذكاء الاصطناعي مع السؤال الحالي
                    if st.session_state.saved_image:
                        response = model.generate_content([system_prompt, st.session_state.saved_image])
                    else:
                        response = model.generate_content(system_prompt)
                        
                    answer = response.text
                except Exception as e:
                    answer = "أنا جاهز ومستعد لمساعدتك في كافة البحوث، الترجمة، والأكواد. يرجى إعادة إرسال الطلب."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            
            # توليد الصوت الذكي لقراءة النص للزائر تلقائياً
            try:
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer[:200])}"
                audio_html = f'<audio src="{tts_url}" autoplay controls style="width:100%; height:30px; margin-top:10px;"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": answer, "audio_html": audio_html})
            except Exception:
                st.session_state.messages.append({"role": "assistant", "content": answer})

# --- الترتيب الاحترافي الثابت والمستقر في الأسفل تماماً (تذييل الصفحة) ---
st.markdown("<br><br><hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)

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

# اسم المطور ظاهر علناً للقراء بخط صغير وأنيق في قاع الصفحة تماماً
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
