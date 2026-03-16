import streamlit as st
from seo_engine import *
from ai_engine import *

st.set_page_config(
    page_title="YouTube AI SEO Tool PRO",
    layout="wide"
)

st.title("🚀 YouTube AI SEO Tool PRO")

st.write("Tạo SEO video chuẩn thuật toán YouTube")

# INPUT
col1, col2 = st.columns(2)

with col1:
    keyword = st.text_input("Từ khóa chính")

with col2:
    channel = st.text_input("Link kênh (optional)")


if st.button("🚀 TẠO SEO VIDEO"):

    st.success("Đang tạo nội dung SEO...")

    # TITLES
    st.header("🔥 Tiêu đề gợi ý")

    titles = generate_titles(keyword) + ai_titles(keyword)

    for t in titles:
        st.write("•", t)

    # TAGS
    st.header("🏷 Tags")

    tags = generate_tags(keyword)

    st.write(", ".join(tags))

    # DESCRIPTION
    st.header("📝 Description")

    desc = generate_description(keyword)

    st.write(desc)

    # SCRIPT
    st.header("🎬 Video Script")

    script = ai_script(keyword)

    st.write(script)


# THUMBNAIL TOOL
st.header("🎨 Thumbnail Prompt Generator")

thumb_text = st.text_input("Text trên thumbnail")

if st.button("Tạo Prompt"):

    prompt = thumbnail_prompt(keyword, thumb_text)

    st.code(prompt)

# DOWNLOAD
st.header("📥 Export SEO")

if st.button("Download SEO Pack"):

    data = f"""
Keyword: {keyword}

Titles:
{titles}

Tags:
{tags}

Description:
{desc}

Script:
{script}
"""

    st.download_button(
        "Download",
        data,
        file_name="youtube_seo.txt"
    )
