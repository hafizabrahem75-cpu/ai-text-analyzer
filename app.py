import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. إعدادات الصفحة وعنوان الموقع الذي يظهر في المتصفح
st.set_page_config(page_title="محلل النصوص الذكي - حافظ السراء", page_icon="🤖", layout="centered")

# --- إضافة القائمة الجانبية (النقاط الثلاث لتغيير اللغة والتواصل) ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات والخيارات")
    # قائمة اختيار اللغة (مبدئياً كواجهة تظهر للمستخدم)
    language = st.selectbox("🌐 تغيير اللغة (Change Language):", ["العربية (Arabic)", "English"])
    
    st.markdown("---")
    st.markdown("### 📞 تواصل معنا")
    st.write("💬 لا تتردد في مراسلتنا لأي استفسار أو تطوير:")
    st.markdown("📱 **رقم التواصل:** [717245252](tel:717245252)")
    
    # رابط صفحتك على فيسبوك المأخوذ من بياناتك السابقة
    st.markdown("🔗 **تابعنا على فيسبوك:** [صفحة المهندس حافظ](https://www.facebook.com/share/1CgpiG9TYR/)")

# --- الواجهة الرئيسية للموقع ---
st.title("🤖 موقع تحليل المشاعر بالذكاء الاصطناعي")
st.write("اكتب أي جملة باللغة العربية، وسيقوم الذكاء الاصطناعي بمعرفة ما إذا كانت إيجابية أم سلبية!")

# 2. بناء وتدريب نموذج الذكاء الاصطناعي (خلف الكواليس)
texts = [
    "هذا البرنامج ممتاز جدا ورائع", "أنا سعيد للغاية بهذا الإنجاز",
    "التطبيق سيء جدا ولا يعمل", "تجربة مستخدم فاشلة ومزعجة",
    "شرح جميل ومبسط شكرا لك", "الخدمة بطيئة والتعامل غير راق",
    "الحمد لله المنتج ممتاز", "لا أنصح به على الإطلاق"
]
labels = [1, 1, 0, 0, 1, 0, 1, 0] # 1 إيجابي، 0 سلبي

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

# 3. صندوق التفاعل مع الزوار
user_input = st.text_input("أدخل العبارة التي تريد تحليلها هنا:", placeholder="مثال: أنا مستمتع جداً ببرمجة الذكاء الاصطناعي...")

# زر التحليل
if st.button("تحليل النص الآن ✨"):
    if user_input.strip() != "":
        # تحويل النص وتوقعه عبر النموذج
        test_X = vectorizer.transform([user_input])
        prediction = model.predict(test_X)
        
        # عرض النتيجة بشكل مرئي جميل
        if prediction[0] == 1:
            st.success("🤖 النتيجة: هذه عبارة **إيجابية** 👍 (شعور رائع!)")
        else:
            st.error("🤖 النتيجة: هذه عبارة **سلبية** 👎 (شعور غير راقٍ أو محبط)")
    else:
        st.warning("رجاءً اكتب جملة أولاً ليتمكن الذكاء الاصطناعي من تحليلها.")

# --- لمستك الخاصة وحقوق الملكية التي ستظهر للعالم ---
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>تم تطوير هذا البرنامج بواسطة المهندس: حافظ السراء</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>جميع الحقوق محفوظة © مشروع ذكاء اصطناعي تفاعلي متكامل 2026</p>", unsafe_allow_html=True)
