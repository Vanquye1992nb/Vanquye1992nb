import streamlit as st
import google.generativeai as genai
import json
import time

# ==============================
# CONFIG UI
# ==============================

st.set_page_config(page_title="AI SEO Youtube", layout="wide")

st.markdown("""
<style>
.stApp{
background-color:#1e212b;
color:white;
}

.card{
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
padding:6px 12px;
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
    st.header("🔑 API KEY")
    api_key = st.text_input("Gemini API Key", type="password")

# ==============================
# LOAD MODEL
# ==============================

@st.cache_resource
def load_model(key):

    genai.configure(api_key=key)

    return genai.GenerativeModel("gemini-2.0-flash")

# ==============================
# JSON PARSER
# ==============================

def extract_json(text):

    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])

    except:
        return None

# ==============================
# AI GENERATE
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
# INPUT FORM
# ==============================

st.markdown('<div class="card">', unsafe_allow_html=True)

col1,col2 = st.columns(2)

with col1:

    language = st.selectbox(
        "Ngôn ngữ",
        ["Vietnamese","English"]
    )

    competitor = st.text_input(
        "Link video đối thủ (optional)"
    )

with col2:

    keyword = st.text_input(
        "Từ khóa chính"
    )

    channel = st.text_input(
        "Link kênh của bạn (optional)"
    )

generate = st.button("🚀 TẠO SEO VIDEO")

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
Language: {language}

Return ONLY JSON:

{{
"titles":["10 viral youtube titles"],
"tags":["25 high search volume youtube tags"],
"hashtags":["10 trending hashtags"],
"pinned":"Pinned comment to increase engagement",
"comment_rival":"Example smart comment to leave on competitor video"
}}

Rules:
Titles under 70 characters
Tags optimized for YouTube search
"""

            if competitor:

                prompt += f"\nAnalyze competitor video: {competitor}"

            result = ai_generate(prompt)

            if result == "ERROR_429":

                st.error("API quá tải. Hãy thử lại sau.")

            elif result.startswith("LỖI"):

                st.error(result)

            else:

                data = extract_json(result)

                if data:

                    st.session_state.seo = data

                else:

                    st.error("AI trả sai định dạng JSON")

# ==============================
# OUTPUT
# ==============================

if "seo" in st.session_state:

    data = st.session_state.seo

    # TITLES

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🏆 10 Tiêu đề gợi ý")

    titles = data.get("titles",[])

    for i,t in enumerate(titles,1):

        st.write(f"{i}. {t}")

    selected_title = st.selectbox(
        "Chọn tiêu đề để viết mô tả",
        titles
    )

    if st.button("📝 Viết mô tả SEO"):

        desc_prompt = f"""
Write SEO YouTube description for:

{selected_title}

Include:
Intro
Main content
Call to action
Hashtags
"""

        desc = ai_generate(desc_prompt)

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

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🏷️ Tags SEO")

    tags = data.get("tags",[])

    for tag in tags:

        st.markdown(
            f'<span class="tag">{tag}</span>',
            unsafe_allow_html=True
        )

    st.text_area(
        "Copy tags",
        ", ".join(tags),
        height=100
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # HASHTAGS

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("#️⃣ Hashtags")

    st.code(" ".join(data.get("hashtags",[])))

    st.subheader("💬 Pinned comment")

    st.info(data.get("pinned",""))

    st.subheader("📌 Comment đối thủ")

    st.write(data.get("comment_rival",""))

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# THUMBNAIL PROMPT
# ==============================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🎨 Thumbnail Prompt Generator")

thumb_text = st.text_input(
    "Text trên thumbnail"
)

style = st.selectbox(
"Phong cách ảnh",
[
"Photorealistic",
"3D Disney",
"Cyberpunk",
"Minimalist"
]
)

if st.button("🖼️ Tạo Prompt Thumbnail"):

    prompt = f"""
YouTube thumbnail for video about {keyword}

Style: {style}

Big bold text: {thumb_text}

High contrast
8k resolution
Cinematic lighting
Eye catching
"""

    st.code(prompt)

st.markdown('</div>', unsafe_allow_html=True)
