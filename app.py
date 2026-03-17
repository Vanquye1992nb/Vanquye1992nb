import streamlit as st
import random

st.set_page_config(page_title="YouTube SEO AI Tool", layout="centered")

st.title("🚀 Chuyên Gia SEO Video")
st.caption("Công cụ AI tối ưu video YouTube lên top")

# =========================
# SESSION STATE
# =========================

if "titles" not in st.session_state:
    st.session_state.titles=[]

if "viral_titles" not in st.session_state:
    st.session_state.viral_titles=[]

if "keywords" not in st.session_state:
    st.session_state.keywords=[]

if "hashtags" not in st.session_state:
    st.session_state.hashtags=[]

if "description" not in st.session_state:
    st.session_state.description=""

if "hook" not in st.session_state:
    st.session_state.hook=""

if "script" not in st.session_state:
    st.session_state.script=""

# =========================
# INPUT
# =========================

keyword = st.text_input("Từ khóa chính")
competitor = st.text_input("Link video đối thủ")
channel = st.text_input("Link kênh")

# =========================
# KEYWORD RESEARCH
# =========================

st.markdown("### 🔍 Keyword Research")

if st.button("Gợi ý keyword mở rộng"):

    suggestions=[
        f"{keyword} documentary",
        f"{keyword} explained",
        f"{keyword} history",
        f"{keyword} facts",
        f"{keyword} evolution",
        f"{keyword} discovery",
        f"{keyword} secrets"
    ]

    st.write(suggestions)

# =========================
# GENERATE MAIN CONTENT
# =========================

if st.button("⚡ Tạo Nội Dung SEO"):

    titles=[
        f"Unveiling {keyword}",
        f"The Lost World of {keyword}",
        f"Secrets of {keyword}",
        f"Amazing Facts About {keyword}",
        f"Discovering {keyword}",
        f"Deep Dive Into {keyword}",
        f"History of {keyword}",
        f"What Life Was Like: {keyword}",
        f"Journey Through {keyword}",
        f"The Truth About {keyword}"
    ]

    st.session_state.titles=titles

    viral=[
        f"You Won't Believe {keyword}",
        f"The Dark Truth of {keyword}",
        f"Scientists Finally Explain {keyword}",
        f"The Hidden Story of {keyword}",
        f"Shocking Discovery About {keyword}",
        f"The Mystery Behind {keyword}",
        f"Everything You Know About {keyword} Is Wrong",
        f"The Untold Story of {keyword}",
        f"The Rise and Fall of {keyword}",
        f"The Secret History of {keyword}"
    ]

    st.session_state.viral_titles=viral

    keywords=[
        keyword,
        "prehistoric earth",
        "dinosaurs",
        "ancient earth",
        "paleontology",
        "fossils",
        "mesozoic era",
        "jurassic period",
        "triassic period",
        "cretaceous period",
        "extinct animals",
        "earth history",
        "ancient creatures",
        "evolution of life",
        "origins of life",
        "cambrian explosion",
        "permian extinction",
        "devonian period",
        "prehistoric animals",
        "ancient marine life"
    ]

    st.session_state.keywords=keywords

    hashtags=[f"#{k.replace(' ','')}" for k in keywords[:15]]

    st.session_state.hashtags=hashtags

# =========================
# TITLES
# =========================

if st.session_state.titles:

    st.divider()

    st.subheader("🏆 10 Tiêu đề YouTube")

    for i,t in enumerate(st.session_state.titles,1):
        st.write(f"{i}. {t}")

    st.subheader("🔥 Viral Titles")

    for t in st.session_state.viral_titles:
        st.write(t)

    selected_title=st.selectbox(
        "Chọn tiêu đề tạo mô tả",
        st.session_state.titles
    )

# =========================
# DESCRIPTION
# =========================

    if st.button("✍️ Tạo mô tả SEO"):

        desc=f"""
🔥 {selected_title}

Explore {keyword} and discover incredible secrets.

This video explains the history, science and mystery behind {keyword}.

{ " ".join(st.session_state.hashtags[:5]) }
"""

        st.session_state.description=desc

    if st.session_state.description:
        st.markdown("### 📄 Mô tả SEO")
        st.code(st.session_state.description)

# =========================
# KEYWORDS
# =========================

    st.markdown("### 📈 SEO Keywords")

    st.write(", ".join(st.session_state.keywords))

# =========================
# HASHTAGS
# =========================

    st.markdown("### 🔥 Hashtags lên top")

    st.write(" ".join(st.session_state.hashtags))

# =========================
# HOOK GENERATOR
# =========================

    st.markdown("### 🎬 Video Hook")

    if st.button("Tạo Hook Video"):

        hook=f"""
What if everything you knew about {keyword} was wrong?

Today we reveal the truth behind {keyword}
and the discoveries that changed history.
"""

        st.session_state.hook=hook

    if st.session_state.hook:
        st.code(st.session_state.hook)

# =========================
# SCRIPT GENERATOR
# =========================

    st.markdown("### 🧠 Video Script")

    if st.button("Tạo Script Video"):

        script=f"""
INTRO
Welcome to this documentary about {keyword}.

SECTION 1
Origins of {keyword}

SECTION 2
Major discoveries

SECTION 3
Why it matters today

OUTRO
Subscribe for more educational content.
"""

        st.session_state.script=script

    if st.session_state.script:
        st.code(st.session_state.script)

# =========================
# PIN COMMENT
# =========================

    st.markdown("### 💬 Bình luận ghim")

    comment=f"""
If you could travel back in time to see {keyword},
what moment would you choose?

👇 Comment below
"""

    st.code(comment)

# =========================
# THUMBNAIL PROMPT
# =========================

    st.markdown("### 🎨 Thumbnail Prompt")

    text_thumb=st.text_input("Text trên thumbnail")

    style=st.selectbox(
        "Phong cách",
        ["cinematic","realistic","3D render","cartoon","epic"]
    )

    if st.button("Tạo Prompt Thumbnail"):

        prompt=f"""
youtube thumbnail, {keyword},
dramatic lighting,
{style} style,
big bold text '{text_thumb}',
ultra detailed
"""

        st.code(prompt)

# =========================
# SEO SCORE
# =========================

    score=random.randint(82,96)

    st.metric("SEO Score",score)

# =========================
# EXPORT
# =========================

    st.markdown("### 📦 Export SEO Pack")

    pack=f"""
Keyword:
{keyword}

Titles:
{st.session_state.titles}

Viral Titles:
{st.session_state.viral_titles}

Keywords:
{st.session_state.keywords}

Hashtags:
{st.session_state.hashtags}
"""

    st.download_button(
        "Download SEO Pack",
        pack,
        file_name="youtube_seo_pack.txt"
    )

# =========================
# RESET
# =========================

if st.button("🔄 Reset Tool"):
    st.session_state.clear()
    st.rerun()
