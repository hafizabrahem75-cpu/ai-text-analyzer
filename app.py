import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الاحترافية الشاملة
st.set_page_config(page_title="منصة حافظ السراء للذكاء الاصطناعي", page_icon="🧠", layout="centered")

# تنسيق واجهة العرض العلوية وتصغير خط العنوان
st.markdown("<h2 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🧠 منصة حافظ السراء للذكاء الاصطناعي الشامل</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 14px;'>مساعدك الخارق الشامل: إجابات ذكية، تحليل لقطات الشاشة، توليد صور، وقراءة صوتية شاملة بدون عجز!</p>", unsafe_allow_html=True)

# ربط النظام بالمفتاح السري وتفعيل أحدث وأقوى نموذج من جوجل Gemini
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام نموذج gemini-1.5-flash المستقر والقوي جداً في فهم الصور والنصوص معاً
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_api = True
    else:
        has_api = False
except Exception:
    has_api = False

# نظام الذاكرة المستمرة للمحادثة وحفظ الصور لمنع اختفائها عند التحديث
if "messages" not in st.session_state:
    st.session_state.messages = []
if "cached_image" not in st.session_state:
    st.session_state.cached_image = None

# عرض الرسائل السابقة في منتصف الشاشة مع الحفاظ على الرسوم والصوتيات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# تفعيل زر رفع الصور ولقطات الشاشة وحفظها فوراً في الذاكرة لمنع مسحها
uploaded_file = st.file_uploader("📸 أرسل لقطة شاشة، كتاب، أو صورة لتحليلها وتعديلها:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.session_state.cached_image = Image.open(uploaded_file)

# صندوق إدخال الأسئلة والأوامر في الأسفل
user_query = st.chat_input("اسألني عن أي شيء، أو اطلب صورة، أو ارفع لقطة شاشة...")

if user_query or st.session_state.cached_image:
    query_text = user_query if user_query else "حلل هذه الصورة واشرحها بالتفصيل وحل ما فيها"
    
    # عرض مدخلات المستخدم
    with st.chat_message("user"):
        st.markdown(query_text)
        if st.session_state.cached_image:
            st.image(st.session_state.cached_image, caption="اللقطة الجاري تحليلها")
            
    # حفظ رسالة المستخدم في الذاكرة
    st.session_state.messages.append({"role": "user", "content": query_text})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        clean_query = query_text.strip()
        
        # حساب توقيت اليمن برمجياً وبشكل مدمج (توقيت جرينتش + 3 ساعات) بدون مكتبات خارجية
        utc_now = datetime.utcnow()
        yemen_now = utc_now + timedelta(hours=3)
        time_str = yemen_now.strftime("%I:%M %p")
        date_str = yemen_now.strftime("%Y-%m-%d")
        
        # 1. حل مشكلة الوقت والساعة فوراً وبشكل شامل
        if any(keyword in clean_query for keyword in ["كم الساعه", "الوقت الان", "الساعه كم", "كم الوقت", "ساعه كم"]):
            answer = f"🕒 الوقت الآن في اليمن هو تمام الساعة: {time_str} \n📅 وتاريخ اليوم هو: {date_str}"
            message_placeholder.markdown(answer)
            
            # تحويل الإجابة لصوت مسموع تلقائياً
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            st.audio(tts_url, format="audio/mp3")
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            
        # 2. الرد الفوري الذكي على التحيات المباشرة
        elif clean_query in ["السلام عليكم", "سلام عليكم", "السلام عليكم ورحمة الله", "سلام"]:
            answer = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا بشمهندس حافظ، أنا منصتك الخارقة وجاهز لكل طلباتك الشاملة."
            message_placeholder.markdown(answer)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer)}"
            st.audio(tts_url, format="audio/mp3")
            st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            
        # 3. ميزة توليد الصور الفائقة الشاملة خلفيات دقيقة (مع التشفير السليم للهندسة)
        elif any(keyword in clean_query for keyword in ["ارسم", "صورة", "صمم", "توليد", "رسمة"]) and not st.session_state.cached_image:
            message_placeholder.markdown("🎨 جاري تخيل ورسم الصورة بدقة احترافية خارقة...")
            try:
                # حل ذكي: إضافة كلمات تجعل السيرفر يهتم بالخلفية بدقة (مثل شوارع صنعاء القديمة)
                enhanced_query = clean_query + " highly detailed, realistic, full background photorealistic"
                encoded_prompt = urllib.parse.quote(enhanced_query)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&private=true"
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": f"ها هي الصورة الاحترافية الشاملة التي صممتها لك لـ: {query_text}", "image": image_url})
                message_placeholder.empty()
            except Exception:
                message_placeholder.markdown("عذراً، واجه محرك الصور ضغطاً، يرجى المحاولة مرة أخرى.")
                
        # 4. العقل الشامل (Gemini): حل المشاكل، البحوث، الترجمة، وقراءة لقطات الشاشة والملفات بدون عجز
        else:
            message_placeholder.markdown("🧠 جاري التفكير والتحليل الشامل كقدوتك Gemini...")
            if has_api:
                try:
                    # تزويد النموذج بالتوقيت الحالي ليكون ذكياً وشاملاً في الإجابة
                    system_prompt = f"التوقيت الحالي في اليمن هو {date_str} {time_str}. أجب مباشرة باللغة العربية وبدون مقدمات ترحيبية أو تكرار للسؤال، وكن شاملاً وذكياً جداً في الإجابة على الطلب التالي: {clean_query}"
                    
                    if st.session_state.cached_image:
                        response = model.generate_content([system_prompt, st.session_state.cached_image])
                    else:
                        response = model.generate_content(system_prompt)
                        
                    answer = response.text
                except Exception:
                    answer = "أنا مستعد لمساعدتك في كافة البحوث والترجمة والأكواد وقراءة الصور، يرجى إعادة إرسال طلبك بوضوح."
            else:
                answer = "⚙️ النظام بانتظار تفعيل المفتاح السري تلقائياً من الإعدادات (Secrets) للبدء."
            
            message_placeholder.markdown(answer)
            
            # توليد الصوت التلقائي لقراءة الإجابة نصياً
            try:
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ar&client=tw-ob&q={urllib.parse.quote(answer[:200])}"
                st.audio(tts_url, format="audio/mp3")
                st.session_state.messages.append({"role": "assistant", "content": answer, "audio": tts_url})
            except Exception:
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # تفريغ ذاكرة الصورة المرفوعة بعد المعالجة الناجحة حتى لا تتكرر تلقائياً
    st.session_state.cached_image = None

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

# اسم المطور ظاهر علناً في قاع الصفحة تماماً
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 0px;'>تم تطوير هذا الروبوت بواسطة المهندس: حافظ السراء © 2026</p>", unsafe_allow_html=True)
