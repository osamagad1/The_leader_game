import streamlit as st
import random
import time
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="لعبة القائد | بودكاست من زكاها",
    page_icon="⭐",
    layout="centered"
)

# --- قائمة المستويات (لزيادة الترفيه) ---
SCENARIOS = {
    # 0-50 نقطة: تحديات شخصية بسيطة
    "المستوى 1: بوابة الشك": [
        "لديك اجتماع مهم غداً. الدخيل يقول: 'ستنسى كل ما ستقوله وستبدو مرتبكاً.'",
        "تأخرت في بدء تمرينك اليومي. الدخيل يقول: 'فات الأوان اليوم، ابدأ غداً.'",
        "شخص انتقد رأيك عبر الإنترنت. الدخيل يقول: 'رأيك دائماً سخيف ولا أحد يأخذك بجدية.'",
        "ارتكبت خطأ صغيراً في تقرير العمل. الدخيل يقول: 'أنت غير كفؤ، وسيكتشفون ذلك قريباً.'",
    ],
    # 51-150 نقطة: تحديات اجتماعية ونفسية
    "المستوى 2: سجن المقارنة": [
        "شاهدت منشوراً لصديق يبدو أكثر نجاحاً منك. الدخيل يقول: 'أنت متأخر جداً في الحياة، ولن تلحق بهم أبداً.'",
        "تشعر بالوحدة في المساء. الدخيل يقول: 'أنت غير جدير بالصداقة، وستظل وحيداً دائماً.'",
        "قمت بتجربة شيء جديد وفشلت. الدخيل يقول: 'هذه ليست موهبتك، توقف عن إحراج نفسك.'",
    ],
    # 151+ نقطة: تحديات الإنجاز والذات العليا
    "المستوى 3: عرش الإنجاز": [
        "تشعر بالملل من الروتين. الدخيل يقول: 'حياتك مملة، ولن تنجز شيئاً ذا معنى أبداً.'",
        "تعتقد أنك غير مستعد للمرحلة القادمة من خطتك. الدخيل يقول: 'الفشل هو الخيار الأكيد، انسحب الآن وحافظ على كرامتك.'",
    ],
}

# --- وظائف مساعدة ---
def determine_level(score):
    if score < 30:
        return "حارس البوابة (مبتدئ)"
    elif score < 100:
        return "قائد الحرس (متمرس)"
    elif score < 200:
        return "حكيم القلعة (خبير)"
    else:
        return "القائد الأعلى (ماستر)"

def get_current_scenario(score):
    if score < 50:
        key = "المستوى 1: بوابة الشك"
    elif score < 150:
        key = "المستوى 2: سجن المقارنة"
    else:
        key = "المستوى 3: عرش الإنجاز"
    
    # اختيار تحدي عشوائي من المستوى المناسب
    challenge = random.choice(SCENARIOS[key])
    return key, challenge

def reset_round():
    st.session_state.stage = 0
    st.session_state.thought = ""
    st.session_state.evidence = ""
    st.session_state.monster_icon = ""

def generate_journal_text():
    text = f"⭐ سجل انتصارات القائد الذاتي\n"
    text += f"القائد: {st.session_state.user_name}\n" # إضافة اسم المستخدم
    text += f"تاريخ: {datetime.now().strftime('%Y-%m-%d')}\n"
    text += f"الرتبة النهائية: {determine_level(st.session_state.score)}\n"
    text += "====================================\n\n"
    
    for i, entry in enumerate(st.session_state.journal, 1):
        text += f"⚔️ المعركة رقم {i} ({entry['level']}):\n"
        text += f"👾 الدخيل (الفكرة السلبية): {entry['thought']}\n"
        text += f"⚖️ دليل البطلان: {entry['evidence']}\n"
        text += f"✅ الفرمان (التوجيه الجديد): {entry['new_belief']}\n"
        text += "------------------------------------\n"
    
    text += "\n💡 تذكر: قد أفلح من زكاها."
    return text

# --- تهيئة متغيرات اللعبة (Session State) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'stage' not in st.session_state: st.session_state.stage = -1 # تغيير البدء إلى -1 (تسجيل الدخول)
if 'thought' not in st.session_state: st.session_state.thought = ""
if 'evidence' not in st.session_state: st.session_state.evidence = ""
if 'monster_icon' not in st.session_state: st.session_state.monster_icon = ""
if 'journal' not in st.session_state: st.session_state.journal = []
if 'user_name' not in st.session_state: st.session_state.user_name = "ضيف" # إضافة اسم المستخدم
if 'user_email' not in st.session_state: st.session_state.user_email = ""


# --- واجهة اللعبة (تم تحسين الـ UI/UX) ---

# الشريط الجانبي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3241/3241151.png", width=80)
    st.title(f"قلعة القائد الذاتي ⭐")
    if st.session_state.user_name != "ضيف":
        st.caption(f"مرحباً، {st.session_state.user_name}!")
    st.markdown("---")
    
    st.metric(label="نقاط الوعي (XP)", value=st.session_state.score)
    st.write(f"**عدد الدخلاء المطرودين:** {len(st.session_state.journal)}")
    st.caption(f"الرتبة الحالية: **{determine_level(st.session_state.score)}**")
    
    # زر تحميل السجل (محلول مشكلة التقرير هنا)
    if st.session_state.journal:
        st.markdown("---")
        st.write("📥 **احتفظ بتوجيهاتك (ملف التقرير جاهز):**")
        st.download_button(
            label="تحميل سجل الإنجازات 📄",
            data=generate_journal_text(),
            file_name=f"Qaid_Journal_{st.session_state.user_name}_{datetime.now().strftime('%d-%m')}.txt",
            mime="text/plain"
        )
    
    st.markdown("---")
    if st.button("إعادة تشغيل اللعبة 🗑️"):
        st.session_state.clear()
        st.rerun()

# المنطقة الرئيسية
st.progress(min(st.session_state.score, 200) / 200, text="التقدم نحو الرتبة التالية...")
st.markdown("---")

# --- مراحل اللعبة ---

# المرحلة -1: تسجيل الدخول (ثانياً)
if st.session_state.stage == -1:
    st.header("🔑 تسجيل الدخول إلى منظومة القيادة")
    st.write("الرجاء إدخال بياناتك لبدء حفظ تقدمك في هذه الجلسة.")
    
    name_input = st.text_input("اسم القائد:", key="name_input_key", placeholder="مثال: يوسف")
    email_input = st.text_input("البريد الإلكتروني (للتوثيق):", key="email_input_key", placeholder="اختياري للتوثيق")
    
    if st.button("ابدأ القيادة! 🚀"):
        if name_input:
            st.session_state.user_name = name_input
            st.session_state.user_email = email_input
            st.session_state.stage = 0
            st.success(f"أهلاً بالقائد {name_input}، مهمتك تبدأ الآن!")
            st.balloons()
            st.rerun()
        else:
            st.warning("الرجاء إدخال اسمك أولاً.")

# المرحلة 0: رصد الفكرة
elif st.session_state.stage == 0:
    current_level, scenario_text = get_current_scenario(st.session_state.score)
    st.subheader(f"🛡️ {current_level} - مهمة رصد الدخيل")
    
    # استخدام سيناريوهات جاهزة
    st.info(f"**السيناريو:** {scenario_text}")
    
    st.write("ما هي الفكرة السلبية التي تولّدت في ذهنك نتيجة لهذا السيناريو؟")
    thought_input = st.text_area("الدخيل (الفكرة السلبية):", placeholder="أدخل الفكرة هنا...")
    
    if st.button("رصد الدخيل 👁️"):
        if thought_input:
            st.session_state.thought = thought_input
            st.session_state.current_level_name = current_level # حفظ اسم المستوى
            st.session_state.stage = 1
            st.rerun()
        else:
            st.warning("الرجاء تحديد الدخيل أولاً، فالقائد لا يتحرك بلا هدف!")

# المرحلة 1: التجسيد
elif st.session_state.stage == 1:
    st.subheader("👾 كشف الهوية (جعل الدخيل سخيفاً)")
    st.markdown(f"**الدخيل المُرصَد:** *{st.session_state.thought}*")
    st.write("اختر شكلاً هزلياً لهذا الدخيل لكسر هيبته:")
    
    # استخدام الأعمدة لتحسين الـ UX وجعل الاختيار بصرياً
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    
    monsters_list = [("🤡", "مهرج سخيف"), ("🧟", "زومبي كسول"), ("👺", "عفريت غاضب"), ("🦜", "ببغاء يثرثر"), ("👶", "طفل مدلل")]
    
    monster_selection = st.radio(
        "اختر شكل الدخيل:",
        options=[m[1] for m in monsters_list],
        format_func=lambda x: f"{[m[0] for m in monsters_list if m[1] == x][0]} {x}",
        key="monster_radio_key"
    )
    
    if st.button("تقييد الدخيل ⛓️"):
        # استخراج الأيقونة فقط
        selected_icon = [m[0] for m in monsters_list if m[1] == monster_selection][0]
        st.session_state.monster_icon = selected_icon
        st.session_state.stage = 2
        st.rerun()

# المرحلة 2: المحاكمة
elif st.session_state.stage == 2:
    st.subheader("⚖️ محكمة القائد (طلب الدليل)")
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.monster_icon}</h1>", unsafe_allow_html=True)
    st.write(f"الدخيل **'{st.session_state.thought}'** يطالب بالبقاء. **أنت القائد.**")
    st.info("اكتب دليلاً واقعياً أو منطقياً يُبطل أو يُخفف من صحة هذه الفكرة السلبية.")
    
    evidence_input = st.text_area("دليل البطلان (التفنيد المنطقي):", height=150, placeholder="مثال: هذا تعميم خاطئ، أنا لدي إنجازات كثيرة مثل... وهي تثبت العكس.")
    
    if st.button("إسقاط التهمة 🔨"):
        if evidence_input:
            st.session_state.evidence = evidence_input
            st.session_state.stage = 3
            st.rerun()
        else:
            st.warning("القائد لا يتخذ قراراً بلا دليل! واجه الدخيل.")

# المرحلة 3: الفرمان والإضافة للسجل
elif st.session_state.stage == 3:
    st.subheader("📜 فرمان القائد (التوجيه الجديد)")
    st.success("تم دحض الفكرة السلبية بالحجة والبرهان!")
    
    st.markdown(f"> **الدخيل المدحوض:** *{st.session_state.thought}*")
    st.write("الآن، أصدر **فرماناً** جديداً وإيجابياً ليحل محل الفكرة المدحوضة ويصبح حقيقة راسخة:")
    
    new_belief = st.text_input("الفكرة الجديدة (التزكية):", placeholder="مثال: أنا أتعلم من أخطائي وأستحق النجاح.", key="new_belief_input")
    
    if st.button("ختم الفرمان وحفظ الانتصار ⭐"):
        if new_belief:
            st.balloons()
            st.session_state.score += 10
            
            # --- إضافة الجولة إلى السجل (تم حل مشكلة التقرير هنا) ---
            entry = {
                "thought": st.session_state.thought,
                "evidence": st.session_state.evidence,
                "new_belief": new_belief,
                "level": st.session_state.current_level_name # حفظ اسم المستوى للمراجعة
            }
            st.session_state.journal.append(entry)
            # -----------------------------
            
            st.success(f"تم تأمين القلعة! +10 نقاط وعي. يمكنك تحميل تقريرك من القائمة الجانبية.")
            
            st.write("---")
            if st.button("مواجهة دخيل آخر 🔄", type="primary"):
                reset_round()
                st.rerun() # هذا يحل مشكلة عدم تحديث الشاشة تلقائياً
