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


# --- تنسيق الواجهة (RTL + تصميم) ---
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    .stTextInput > div > div > input {
        text-align: right;
    }
    .stTextArea > div > div > textarea {
        text-align: right;
    }
    .stMarkdown, .stButton, .stDownloadButton {
        text-align: right !important;
    }
    div[data-testid="stMetricValue"] {
        text-align: center;
    }
    /* تصميم زر التحميل ليكون مميزاً */
    button[data-testid="stBaseButton-secondary"] {
        border-color: #4CAF50;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)


# --- تهيئة متغيرات اللعبة (Session State) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'stage' not in st.session_state:
    st.session_state.stage = 0 
if 'thought' not in st.session_state:
    st.session_state.thought = ""
if 'evidence' not in st.session_state:
    st.session_state.evidence = ""
if 'monster_icon' not in st.session_state:
    st.session_state.monster_icon = ""
if 'journal' not in st.session_state:
    st.session_state.journal = []


# --- وظائف مساعدة ---
def determine_level(score):
    # الرتب الأصلية (تم استعادتها)
    if score < 30:
        return "حارس البوابة (مبتدئ)"
    elif score < 100:
        return "قائد الحرس (متمرس)"
    elif score < 200:
        return "حكيم القلعة (خبير)"
    else:
        # تغيير طفيف للماستر ليتناسب مع "القائد" بدلاً من "الملك"
        return "القائد الأعلى (ماستر)"


def reset_round():
    st.session_state.stage = 0
    st.session_state.thought = ""
    st.session_state.evidence = ""
    st.session_state.monster_icon = ""


def generate_journal_text():
    text = f"⭐ سجل انتصارات القائد الذاتي\n"
    text += f"تاريخ: {datetime.now().strftime('%Y-%m-%d')}\n"
    text += f"الرتبة النهائية: {determine_level(st.session_state.score)}\n"
    text += "====================================\n\n"
    
    for i, entry in enumerate(st.session_state.journal, 1):
        text += f"⚔️ المعركة رقم {i}:\n"
        text += f"👾 الدخيل (الفكرة السلبية): {entry['thought']}\n"
        text += f"⚖️ دليل البطلان: {entry['evidence']}\n"
        text += f"✅ الفرمان (التوجيه الجديد): {entry['new_belief']}\n"
        text += "------------------------------------\n"
    
    text += "\n💡 تذكر: قد أفلح من زكاها."
    return text


# --- واجهة اللعبة ---


# الشريط الجانبي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3241/3241151.png", width=80)
    st.title("قلعة القائد الذاتي ⭐") # اسم جديد يجمع بين القائد والقلعة
    st.markdown("---")
    
    st.write(f"**عدد الدخلاء المطرودين:** {len(st.session_state.journal)}")
    
    # زر تحميل السجل
    if st.session_state.journal:
        st.markdown("---")
        st.write("📥 **احتفظ بتوجيهاتك:**")
        st.download_button(
            label="تحميل سجل الإنجازات 📄",
            data=generate_journal_text(),
            file_name=f"my_leadership_journal_{datetime.now().strftime('%d-%m')}.txt",
            mime="text/plain"
        )


# المنطقة الرئيسية
col1, col2 = st.columns([1, 3])
with col1:
    st.metric(label="نقاط الوعي (XP)", value=st.session_state.score)
with col2:
    st.title("🛡️ لعبة القائد")
    st.caption(f"الرتبة الحالية: **{determine_level(st.session_state.score)}**")


st.progress(min(st.session_state.score, 200) / 200)
st.markdown("---")


# --- مراحل اللعبة ---


# المرحلة 0: رصد الفكرة
if st.session_state.stage == 0:
    st.subheader("🚨 صافرات الإنذار!")
    st.write("هناك 'دخيل' يحاول التسلل إلى **عرش القائد**. ما هي الفكرة السلبية؟") # تعديل على "عرش القائد"
    thought_input = st.text_input("اكتب الفكرة هنا:", placeholder="مثال: أنا فاشل ولن أنجح أبداً...")
    
    if st.button("رصد الدخيل 👁️"):
        if thought_input:
            st.session_state.thought = thought_input
            st.session_state.stage = 1
            st.rerun()
        else:
            st.warning("الرجاء تحديد الدخيل أولاً، فالقائد لا يتحرك بلا هدف!")


# المرحلة 1: التجسيد
elif st.session_state.stage == 1:
    st.subheader("👾 كشف الهوية")
    st.write(f"الفكرة: **'{st.session_state.thought}'** تم رصدها.")
    st.write("اختر شكلاً هزلياً لهذا الدخيل لكسر نفوذه:")
    monsters = ["🤡 مهرج سخيف", "🧟 زومبي كسول", "👺 عفريت غاضب", "🦜 ببغاء يثرثر", "👶 طفل مدلل"]
    selected_monster = st.radio("", monsters)
    
    if st.button("تقييد الدخيل ⛓️"):
        st.session_state.monster_icon = selected_monster.split()[0]
        st.session_state.stage = 2
        st.rerun()


# المرحلة 2: المحاكمة
elif st.session_state.stage == 2:
    st.subheader("⚖️ محكمة القائد") # تغيير الاسم
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.monster_icon}</h1>", unsafe_allow_html=True)
    st.write(f"الدخيل **'{st.session_state.thought}'** يحاول الدفاع عن نفسه.")
    st.write("**أنت القائد. اطلب الدليل القاطع الذي يثبت أن هذه الفكرة كاذبة:**")
    
    evidence_input = st.text_area("دليل البطلان (التفنيد المنطقي):", placeholder="مثال: هذا تعميم خاطئ، أنا لدي إنجازات كثيرة و...")
    
    if st.button("إسقاط التهمة 🔨"):
        if evidence_input:
            st.session_state.evidence = evidence_input
            st.session_state.stage = 3
            st.rerun()
        else:
            st.warning("القائد لا يتخذ قراراً بلا دليل! واجه الدخيل.")


# المرحلة 3: الفرمان والإضافة للسجل
elif st.session_state.stage == 3:
    st.subheader("📜 فرمان القائد") # تغيير الاسم
    st.success("تم دحض الفكرة السلبية بالحجة والبرهان!")
    st.write(f"الآن، أصدر **فرماناً** جديداً وإيجابياً ليحل محل: **'{st.session_state.thought}'**") # تعديل على "فرمان"
    
    new_belief = st.text_input("الفكرة الجديدة (التزكية):", placeholder="مثال: أنا أتعلم من أخطائي وأستحق النجاح.")
    
    if st.button("ختم الفرمان وحفظ الانتصار ⭐"): # تعديل على "فرمان"
        if new_belief:
            st.balloons()
            st.session_state.score += 10
            
            # --- إضافة الجولة إلى السجل ---
            entry = {
                "thought": st.session_state.thought,
                "evidence": st.session_state.evidence,
                "new_belief": new_belief
            }
            st.session_state.journal.append(entry)
            # -----------------------------
            
            st.success(f"تم تأمين القلعة! +10 نقاط وعي.") # تعديل على "القلعة"
            
            if len(st.session_state.journal) == 1:
                st.info("💡 نصيحة: لقد ظهر زر لتحميل سجل الإنجازات في القائمة الجانبية (Sidebar)!")
            
            time.sleep(2)
            st.write("---")
            if st.button("مواجهة دخيل آخر 🔄"):
                reset_round()
                st.rerun()