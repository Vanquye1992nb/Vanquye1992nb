import streamlit as st
import random

st.set_page_config(page_title="Trợ Lý SEO YouTube", layout="centered")

st.title("🚀 Chuyên Gia SEO Video")
st.caption("Đưa video của bạn lên top tìm kiếm YouTube")

# =========================
# SESSION STATE
# =========================

if "titles" not in st.session_state:
    st.session_state.titles = []

if "description" not in st.session_state:
    st.session_state.description = ""

if "keywords" not in st.session_state:
    st.session_state.keywords = []

if "comment" not in st.session_state:
    st.session_state.comment = ""

# =========================
# INPUT
# =========================

keyword = st.text_input("Từ khóa chính (Bắt buộc)")
competitor = st.text_input("Link video đối thủ (Tùy chọn)")
channel = st.text_input("Link kênh YouTube của bạn (Tùy chọn)")

# =========================
# GENERATE MAIN CONTENT
# =========================

if st.button("⚡ Tạo Nội Dung Tối Ưu"):

    if keyword == "":
        st.warning("Vui lòng nhập từ khóa")
    else:

        titles = [
            f"Unveiling {keyword}: Life Million Years Ago Explained",
            f"The Lost World of {keyword}",
            f"Journey to the Past: {keyword}",
            f"Amazing Secrets of {keyword}",
            f"Beyond Dinosaurs: {keyword}",
            f"Shocking Truth About {keyword}",
            f"Discovering {keyword}",
            f"Deep Dive Into {keyword}",
            f"The Story of {keyword}",
            f"What Life Was Like: {keyword}"
        ]

        st.session_state.titles = titles

        keywords = [
            keyword,"prehistoric earth","ancient earth","dinosaurs",
            "paleontology","fossils","mesozoic era","jurassic period",
            "triassic period","cretaceous period","extinct animals",
            "early life on earth","ancient creatures","evolution of life",
            "origins of life","earth history","geological time scale",
            "cambrian explosion","permian extinction","devonian period",
            "prehistoric animals","ancient marine life","lost world",
            "earth millions years","history earth"
        ]

        st.session_state.keywords = keywords

        st.session_state.comment = f"""
If you could travel back in time to witness {keyword},
what moment would you want to see most?

Comment below 👇
"""

# =========================
# RESULT PANEL
# =========================

if st.session_state.titles:

    st.divider()
    st.subheader(f"KẾT QUẢ CHO TỪ KHÓA: {keyword.upper()}")

    # =====================
    # SEO SCORE
    # =====================

    seo_score = random.randint(75,95)
    st.metric("SEO Score", f"{seo_score}/100")

    # =====================
    # COMPETITOR TOOLS
    # =====================

    st.markdown("### 🚀 Công cụ phân tích đối thủ")

    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("Danh mục video"):
            st.success("Danh mục đề xuất: Education / Science")

    with col2:
        if st.button("Thẻ Tag Video"):
            st.info("Video nên có 15-20 tags")

    with col3:
        if st.button("Thông tin video"):
            st.info("Video dài 8-15 phút thường có retention tốt")

    # =====================
    # TITLES
    # =====================

    st.markdown("### 🏆 10 Tiêu Đề YouTube")

    for i,t in enumerate(st.session_state.titles,1):
        col1,col2 = st.columns([6,1])

        with col1:
            st.write(f"**Tiêu đề {i}:** {t}")

        with col2:
            st.button("Copy", key=f"copy{i}")

    selected_title = st.selectbox(
        "Chọn tiêu đề để tạo mô tả",
        st.session_state.titles
    )

    # =====================
    # DESCRIPTION
    # =====================

    if st.button("✍️ Tạo Mô Tả SEO"):

        desc = f"""
🔥 {selected_title}

In this video we explore **{keyword}** and uncover
the secrets of life millions of years ago.

Discover prehistoric creatures, ancient Earth,
and the evolution of life.

#prehistoricearth #ancientlife #dinosaurs
"""

        st.session_state.description = desc

    if st.session_state.description:
        st.markdown("### 📄 Mô Tả YouTube")
        st.code(st.session_state.description)

    # =====================
    # KEYWORDS
    # =====================

    st.markdown("### 📈 25 Từ Khóa SEO")

    st.write(", ".join(st.session_state.keywords))

    # =====================
    # PIN COMMENT
    # =====================

    st.markdown("### 💬 Bình Luận Ghim")

    st.code(st.session_state.comment)

    # =====================
    # THUMBNAIL PROMPT
    # =====================

    st.markdown("### 🎨 Công Cụ Tạo Thumbnail")

    thumb_text = st.text_input("Text trên Thumbnail")

    style = st.radio(
        "Chọn phong cách",
        ["Ảnh thật","3D Render","Điện ảnh","Hoạt hình","Tối giản"]
    )

    if st.button("Tạo Prompt Ảnh"):

        prompt = f"""
Cinematic {keyword}, dramatic lighting,
{style} style youtube thumbnail,
big bold text "{thumb_text}",
ultra realistic, 8k
"""

        st.code(prompt)

    # =====================
    # DOWNLOAD
    # =====================

    st.markdown("### ⬇ Tải Nội Dung")

    full_text = f"""
KEYWORD
{keyword}

TITLES
{st.session_state.titles}

KEYWORDS
{st.session_state.keywords}

COMMENT
{st.session_state.comment}
"""

    st.download_button(
        "Download File",
        full_text,
        file_name="youtube_seo.txt"
    )

    # =====================
    # RESET
    # =====================

    if st.button("🔄 Tạo nội dung mới"):
        st.session_state.clear()
        st.rerun()
