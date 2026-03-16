import streamlit as st
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="YouTube AI SEO Tool PRO",
    page_icon="🚀",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🚀 YouTube AI SEO Tool PRO")
st.write("Tạo SEO video chuẩn thuật toán YouTube")

# ---------- FUNCTIONS ----------

def generate_titles(keyword):

    titles = [
        f"{keyword} - Hướng dẫn đầy đủ cho người mới",
        f"5 bí mật về {keyword} mà ít ai biết",
        f"Cách học {keyword} nhanh nhất",
        f"{keyword} từ A-Z",
        f"Sự thật về {keyword}",
        f"{keyword} trong 10 phút",
        f"Top 10 điều thú vị về {keyword}",
        f"{keyword} cho người mới bắt đầu",
        f"Chiến lược {keyword} hiệu quả",
        f"Tất cả về {keyword}"
    ]

    return titles


def generate_tags(keyword):

    tags = [
        keyword,
        f"{keyword} tutorial",
        f"{keyword} guide",
        f"{keyword} tips",
        f"{keyword} beginner",
        f"learn {keyword}",
        f"{keyword} vietnam",
        f"{keyword} youtube",
        f"{keyword} strategy",
        f"{keyword} secrets"
    ]

    return tags


def generate_description(keyword):

    return f"""
Video này nói về **{keyword}**

Trong video bạn sẽ học:

• {keyword} là gì  
• Cách bắt đầu với {keyword}  
• Những sai lầm phổ biến  
• Mẹo nâng cao  

Đăng ký kênh để học thêm nhiều kiến thức hữu ích.
"""


def generate_script(keyword):

    script = f"""
🎬 INTRO
Hôm nay chúng ta sẽ tìm hiểu về {keyword}.

📚 CONTENT

1️⃣ {keyword} là gì  
2️⃣ Vì sao {keyword} quan trọng  
3️⃣ Cách áp dụng {keyword} hiệu quả  

🚀 OUTRO
Nếu video hữu ích hãy like và subscribe kênh.
"""

    return script


def generate_thumbnail_prompt(keyword, text):

    return f"""
YouTube thumbnail

Topic: {keyword}
Text: {text}

Bright colors
High contrast
Shocked expression
Professional YouTube thumbnail
"""


# ---------- INPUT UI ----------

st.header("📥 Nhập thông tin")

col1, col2 = st.columns(2)

with col1:
    keyword = st.text_input("Từ khóa chính")

with col2:
    channel = st.text_input("Link kênh (optional)")


# ---------- GENERATE SEO ----------

if st.button("🚀 TẠO SEO VIDEO"):

    if keyword == "":
        st.warning("Hãy nhập từ khóa")
    else:

        st.success("Đang tạo nội dung SEO...")

        titles = generate_titles(keyword)

        st.subheader("🔥 Tiêu đề video")

        for t in titles:
            st.write("•", t)


        tags = generate_tags(keyword)

        st.subheader("🏷 Tags SEO")

        st.write(", ".join(tags))


        desc = generate_description(keyword)

        st.subheader("📝 Description")

        st.write(desc)


        script = generate_script(keyword)

        st.subheader("🎬 Video Script")

        st.write(script)


        # SAVE SESSION
        st.session_state["titles"] = titles
        st.session_state["tags"] = tags
        st.session_state["desc"] = desc
        st.session_state["script"] = script


# ---------- THUMBNAIL TOOL ----------

st.header("🎨 Thumbnail Prompt Generator")

thumb_text = st.text_input("Text trên thumbnail")

if st.button("Tạo Prompt Thumbnail"):

    if keyword == "":
        st.warning("Nhập keyword trước")
    else:

        prompt = generate_thumbnail_prompt(keyword, thumb_text)

        st.code(prompt)


# ---------- DOWNLOAD SEO PACK ----------

st.header("📥 Download SEO Pack")

if st.button("Tải xuống SEO"):

    if "titles" in st.session_state:

        data = f"""
Keyword: {keyword}

Titles:
{st.session_state['titles']}

Tags:
{st.session_state['tags']}

Description:
{st.session_state['desc']}

Script:
{st.session_state['script']}
"""

        st.download_button(
            "Download File",
            data,
            file_name="youtube_seo_pack.txt"
        )

    else:

        st.warning("Hãy tạo SEO trước")
