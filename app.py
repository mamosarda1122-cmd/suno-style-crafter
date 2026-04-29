import streamlit as st
from config import STYLE_TEMPLATES, MAX_CHARS_DETAILED, MAX_CHARS_SUNO
from style_generator import generate_detailed_style, compress_for_suno

st.set_page_config(page_title="Suno Style Crafter", page_icon="🎵", layout="wide")

st.title("🎵 Suno Style Crafter")
st.markdown("**تطبيق احترافي لتوليد style descriptions للأغاني باستخدام AI**")
st.markdown("---")

# ====== القسم الأول: اختيار النموذج ======
st.subheader("1️⃣ اختر طريقة البدء")
start_mode = st.radio(
    "",
    ["ابدأ من template جاهز", "ابدأ من الصفر"],
    horizontal=True,
    label_visibility="collapsed"
)

# المتغيرات الأساسية
mood = ""
genre = ""
tempo = ""
voice = ""
instruments = ""
mixing = ""

if start_mode == "ابدأ من template جاهز":
    selected_template = st.selectbox("اختر الستايل", list(STYLE_TEMPLATES.keys()))
    template = STYLE_TEMPLATES[selected_template]
    mood = template["mood"]
    genre = template["genre"]
    tempo = template["tempo"]
    voice = template["voice"]
    instruments = template["instruments"]
    mixing = template["mixing"]
    st.success(f"تم تحميل: {selected_template}")
else:
    mood = st.text_input("المزاج / اللغة / اللهجة", placeholder="مثال: ساخر، غاضب، لهجة أردنية-مصرية مختلطة")
    genre = st.text_input("النوع الموسيقي (Genre)", placeholder="مثال: Arabic-English protest rap duet")
    tempo = st.text_input("السرعة / الإيقاع", placeholder="مثال: 88 BPM, dark trap soul")
    voice = st.text_input("الصوت / الأصوات", placeholder="مثال: male-female alternating, cold sarcasm vs explosive")
    instruments = st.text_input("الآلات", placeholder="مثال: heavy 808 bass, punchy snare, oud riff minor key")
    mixing = st.text_input("المكساج / الإنتاج", placeholder="مثال: raw vocals, zero autotune, silence before punchlines")

# ====== القسم الثاني: كلمات الأغنية ======
st.markdown("---")
st.subheader("2️⃣ ألصق كلمات الأغنية")
lyrics = st.text_area(
    "Lyrics (الكلمات)",
    placeholder="الصق كلمات الأغنية هنا...
التطبيق يستخدمها فقط لفهم المزاج العام، لا يتم ذكرها في الـ style",
    height=250,
    max_chars=5000
)

# ====== القسم الثالث: توليد الستايل ======
st.markdown("---")
st.subheader("3️⃣ توليد الـ Style")

if st.button("🎛️ توليد الستايل التفصيلي + المضغوط", type="primary", use_container_width=True):
    if not lyrics.strip():
        st.error("يرجى إدخال الكلمات أولاً!")
    elif not genre or not tempo:
        st.error("يرجى ملء نوع الموسيقى والإيقاع!")
    else:
        with st.spinner("⏳ جاري توليد الستايل التفصيلي..."):
            try:
                detailed = generate_detailed_style(
                    lyrics=lyrics,
                    mood=mood,
                    genre=genre,
                    tempo=tempo,
                    voice=voice,
                    instruments=instruments,
                    mixing=mixing
                )
                st.session_state["detailed"] = detailed
                st.session_state["suno"] = None
                st.success("✅ تم توليد الستايل التفصيلي!")
            except Exception as e:
                st.error(f"خطأ: {e}")

# ====== القسم الرابع: عرض النتائج ======
if "detailed" in st.session_state and st.session_state["detailed"]:
    st.markdown("---")
    st.subheader("4️⃣ النتائج")

    tab1, tab2 = st.tabs(["📋 النسخة التفصيلية", "🚀 النسخة الجاهزة للـ Suno (≤1000 حرف)"])

    with tab1:
        st.text_area("Detailed Style (نسخ كامل)", st.session_state["detailed"], height=400, key="detailed_box")
        st.caption(f"الطول: {len(st.session_state['detailed'])} / {MAX_CHARS_DETAILED} حرف")
        st.button("📋 نسخ التفصيلي", on_click=lambda: st.write("<!-- copied -->"), key="copy_detailed_btn")

    with tab2:
        if st.session_state.get("suno") is None:
            if st.button("🗜️ اضغط الآن إلى 1000 حرف", key="compress_btn"):
                with st.spinner("⏳ جاري الضغط الذكي..."):
                    try:
                        suno = compress_for_suno(st.session_state["detailed"])
                        st.session_state["suno"] = suno
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ في الضغط: {e}")
        else:
            st.text_area("Suno-Ready Style", st.session_state["suno"], height=200, key="suno_box")
            st.caption(f"الطول: {len(st.session_state['suno'])} / {MAX_CHARS_SUNO} حرف")
            st.button("📋 نسخ نسخة Suno", on_click=lambda: st.write("<!-- copied -->"), key="copy_suno_btn")

# ====== الفوتر ======
st.markdown("---")
st.caption("🔒 100% مجاني | يعمل على Groq API Free Tier + Streamlit Cloud | صنع بـ ❤️ للموسيقيين العرب")
