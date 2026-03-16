import streamlit as st
import google.generativeai as genai
import json
import time

# ==============================
# CONFIG UI
# ==============================

st.set_page_config(page_title="SEO Youtube AI", layout="wide")

st.markdown("""
<style>
.stApp{
background-color:#1e212b;
color:white;
}
.glass{
background:rgba(30,41,59,0.7);
padding:25px;
border-radius:15px;
border:1px solid #475569;
margin-bottom:20px;
}
.title{
text-align:center;
font-size:34px;
font-weight:800;
color:#f1c40f;
}
.tag{
background:#334155;
padding:5px 10px;
border-radius:12px;
margin:4px;
display:inline-block;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🚀 AI SEO YOUTUBE TOOL</p>', unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("Gemini API Key", type="password")

# ==============================
# LOAD MODEL (CACHE)
# ==============================

@st.cache_resource
def load_model(key):
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# SAFE JSON PARSER
# ==============================

def extract_json(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except:
        return None

# ==============================
# AI CALL
# ==============================

def ai_generate(prompt):

    model = load_model(api_key)

    for i in range(3):

        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:

            if "429" in str(e):
                time.sleep(5)
            else:
                return f"LỖI: {e}"

    return "ERROR_429"

# ==============================
# INPUT
# ==============================

st.markdown('<div class="glass">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    lang = st.selectbox(
        "Ngôn ngữ",
        ["Vietnamese", "English"]
    )

    competitor = st.text_input(
        "Link video đối thủ (tùy chọn)"
    )

with col2:

    keyword = st.text_input(
        "Từ khóa chính"
    )

    channel = st.text_input(
        "Link kênh của bạn (tùy chọn)"
    )

generate = st.button("🚀 TẠO SEO")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# GENERATE SEO
# ==============================

if generate:

    if keyword == "" or api_key == "":
        st.warning("Vui lòng nhập keyword và API key")

    else:

        with st.spinner("AI đang phân tích SEO..."):

            prompt = f"""

You are a professional YouTube SEO expert.

Keyword: {keyword}
Language: {lang}

Return ONLY JSON:

{{
"titles":["10 viral YouTube titles optimized for CTR"],
"tags":["25 high search volume tags"],
"hashtags":["10 trending hashtags"],
"pinned":"Pinned comment to increase engagement",
"comment_rival":"Example smart comment to leave on competitor video"
}}

Rules:
- Titles under 70 characters
- Tags optimized for YouTube search

"""

            if competitor:
                prompt += f"\nAnalyze competitor video: {competitor}"

            res = ai_generate(prompt)

            if res == "ERROR_429":

                st.error("API quá tải. Hãy đợi vài giây.")

            elif res.startswith("LỖI"):

                st.error(res)

            else:

                data = extract_json(res)

                if data:
                    st.session_state.seo = data
                else:
                    st.error("AI trả dữ liệu sai định dạng")

# ==============================
# OUTPUT
# ==============================

if "seo" in st.session_state:

    data = st.session_state.seo

    # TITLES

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("🏆 Tiêu đề gợi ý")

    titles = data.get("titles", [])

    for i, t in enumerate(titles, 1):
        st.write(f"{i}. {t}")

    selected_title = st.selectbox(
        "Chọn tiêu đề để viết mô tả",
        titles
    )

    if st.button("📝 Viết mô tả"):

        prompt = f"""
Write a YouTube SEO description for title:

{selected_title}

Include:
- intro
- main content
- call to action
- hashtags
"""

        desc = ai_generate(prompt)

        if desc:
            st.session_state.desc = desc

    if "desc" in st.session_state:

        st.text_area(
            "Description",
            st.session_state.desc,
            height=200
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # TAGS

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("🏷 Tags")

    tags = data.get("tags", [])

    for tag in tags:
        st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)

    st.text_area(
        "Copy Tags",
        ", ".join(tags),
        height=100
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # HASHTAGS

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("#️⃣ Hashtags")

    st.code(" ".join(data.get("hashtags", [])))

    st.subheader("💬 Pinned Comment")

    st.info(data.get("pinned", ""))

    st.subheader("📌 Comment đối thủ")

    st.write(data.get("comment_rival", ""))

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# THUMBNAIL PROMPT
# ==============================

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("🎨 Thumbnail Prompt")

text_thumb = st.text_input("Text trên thumbnail")

style = st.selectbox(
"Phong cách",
[
"Photorealistic",
"3D Disney",
"Cyberpunk",
"Minimalist"
]
)

if st.button("🖼 Tạo Prompt"):

    prompt = f"""
YouTube thumbnail for video about {keyword}

Style: {style}

Big bold text: {text_thumb}

High contrast
Cinematic lighting
8k resolution
Viral youtube thumbnail
"""

    st.code(prompt)

st.markdown('</div>', unsafe_allow_html=True)
