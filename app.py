import streamlit as st
import random

st.set_page_config(
    page_title="YouTube SEO Tool PRO",
    layout="wide"
)

st.title("🎥 Chuyên Gia SEO Video")

st.write("Đưa video của bạn lên top tìm kiếm YouTube")

# INPUT
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Chọn ngôn ngữ",
        ["Tiếng Việt", "English"]
    )

with col2:
    keyword = st.text_input(
        "Từ khóa chính (bắt buộc)"
    )

competitor = st.text_input("Link video đối thủ (tùy chọn)")
channel = st.text_input("Link kênh YouTube của bạn (tùy chọn)")

# BUTTON
if st.button("Tạo Nội Dung Tối Ưu"):

    st.header(f"KẾT QUẢ TỐI ƯU CHO TỪ KHÓA: {keyword}")

    # TITLES
    st.subheader("🔥 Tiêu đề YouTube hấp dẫn")

    titles = [
        f"The Truth About {keyword}",
        f"Unveiling {keyword}: Secrets Revealed",
        f"{keyword} Explained in 10 Minutes",
        f"The Lost World of {keyword}",
        f"Beyond Dinosaurs: {keyword}",
        f"Amazing {keyword} Facts",
        f"The Rise of {keyword}",
        f"{keyword} Documentary",
        f"The History of {keyword}",
        f"What Scientists Discovered About {keyword}"
    ]

    for t in titles:
        st.write("•", t)

    # KEYWORDS
    st.subheader("🔎 25 TỪ KHÓA TÌM KIẾM CAO")

    keywords = [
        keyword,
        "prehistoric earth",
        "ancient earth",
        "earth history",
        "paleontology",
        "dinosaurs",
        "fossils",
        "ancient animals",
        "evolution of life",
        "geological timeline",
        "cambrian explosion",
        "permian extinction",
        "mesozoic era",
        "triassic period",
        "jurassic period",
        "cretaceous period",
        "ancient creatures",
        "earth evolution",
        "science documentary",
        "ancient oceans",
        "life million years ago",
        "prehistoric animals",
        "history of earth",
        "earth timeline",
        "ancient life"
    ]

    st.write(", ".join(keywords))

    # DESCRIPTION
    st.subheader("📝 YouTube Description")

    description = f"""
In this video we explore **{keyword}** and uncover the secrets of ancient Earth.

Watch to discover:
- Amazing facts about {keyword}
- The history behind it
- How it shaped the planet

Subscribe for more science documentaries.
"""

    st.write(description)

    # PINNED COMMENT
    st.subheader("💬 Bình luận ghim")

    comment = f"""
What do you think about **{keyword}**?

Let us know in the comments below!

👍 Like  
🔔 Subscribe  
📢 Share with friends
"""

    st.write(comment)

    # HASHTAGS
    st.subheader("🏷 Hashtags")

    hashtags = [
        f"#{keyword}",
        "#science",
        "#history",
        "#earth",
        "#documentary"
    ]

    st.write(" ".join(hashtags))

    # THUMBNAIL
    st.subheader("🎨 Công cụ tạo Thumbnail")

    thumb_text = st.text_input("Văn bản trên Thumbnail")

    style = st.selectbox(
        "Phong cách",
        ["Ảnh thật", "3D Render", "Điện ảnh", "Hoạt hình", "Tối giản"]
    )

    if st.button("Tạo Prompt Thumbnail"):

        prompt = f"""
Viral YouTube thumbnail

Topic: {keyword}
Text: {thumb_text}
Style: {style}

High contrast lighting
Shocked face
Bright colors
Professional YouTube thumbnail
"""

        st.code(prompt)

    # DOWNLOAD
    st.download_button(
        "⬇ Tải toàn bộ nội dung",
        data=str(titles) + str(keywords) + description + comment,
        file_name="youtube_seo.txt"
    )
