import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN (Theo ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s; height: 3.5em; }
    
    /* Màu nút bấm chuẩn ảnh 844 */
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    .desc-output { background: #0f172a; padding: 15px; border-radius: 10px; border-left: 5px solid #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG XỬ LÝ AI THÔNG MINH (CHỐNG LỖI 404 & 429) ---
def get_ai_response(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        # Sửa lỗi 404: Sử dụng tên model ổn định nhất
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        # Sửa lỗi 429: Bắt lỗi ResourceExhausted
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return "ERROR_QUOTA"
        return f"LỖI: {error_msg}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 CÀI ĐẶT")
    api_key = st.text_input("Nhập Gemini API Key", type="password")
    st.info("Mẹo: Nếu dùng bản Free, hãy chờ 60 giây giữa mỗi lần tạo nội dung.")

# KHỐI 1: NHẬP LIỆU (Theo ảnh 843)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: cách làm bánh flan")
        channel = st.text_input("Tên/Link kênh của bạn")
    
    if st.button("🚀 TẠO NỘI DUNG TỐI ƯU", use_container_width=True):
        if not (kw and api_key):
            st.warning("Vui lòng nhập API Key và Từ khóa!")
        else:
            with st.spinner("Đang phân tích dữ liệu SEO chuyên sâu..."):
                prompt = f"""Bạn là chuyên gia SEO Youtube. Hãy phân tích '{kw}' ({lang}). 
                Trả về JSON thuần túy (không kèm lời dẫn):
                {{
                    "titles": ["10 tiêu đề thu hút"],
                    "tags": ["25 tags SEO"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "Mẫu bình luận ghim kêu gọi đăng ký",
                    "comment_rival": "Bình luận mẫu phản hồi khán giả"
                }}"""
                res = get_ai_response(api_key, prompt)
                
                if res == "ERROR_QUOTA":
                    st.error("⚠️ Bạn đã dùng hết hạn mức API miễn phí (Lỗi 429). Hãy đợi 1 phút rồi thử lại.")
                elif "LỖI:" in res:
                    st.error(res)
                else:
                    try:
                        # Tách lấy phần JSON an toàn bằng Regex
                        json_match = re.search(r'\{.*\}', res, re.DOTALL)
                        if json_match:
                            st.session_state.seo_data = json.loads(json_match.group())
                            st.session_state.kw = kw
                        else: st.error("AI trả về định dạng không khớp. Hãy bấm lại nút.")
                    except: st.error("Lỗi xử lý dữ liệu AI. Vui lòng thử lại.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: HIỂN THỊ KẾT QUẢ (Theo ảnh 844, 845, 846)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Ba nút chức năng phụ (Màu chuẩn ảnh 844)
    cb1, cb2, cb3 = st.columns(3)
    with cb1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with cb2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with cb3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị Tiêu đề
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🏅 10 TIÊU ĐỀ CHO TỪ KHÓA: {st.session_state.kw.upper()}")
    for i, t in enumerate(data.get('titles', []), 1):
        st.write(f"**Tiêu đề {i}:** {t}")
    
    st.divider()
    # Chọn tiêu đề tạo mô tả
    sel_title = st.selectbox("Chọn tiêu đề để viết mô tả:", data.get('titles', []))
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("AI đang soạn mô tả chuẩn SEO..."):
            desc_prompt = f"Viết mô tả Youtube chuẩn SEO cho: '{sel_title}'. Gồm: Giới thiệu, Nội dung chính, Kêu gọi hành động."
            desc_res = get_ai_response(api_key, desc_prompt)
            if desc_res == "ERROR_QUOTA": st.error("⚠️ Quá tải API! Hãy chờ 1 chút.")
            else: st.session_state.gen_desc = desc_res
    
    if 'gen_desc' in st.session_state:
        st.markdown(f'<div class="desc-output">{st.session_state.gen_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị Tags & Hashtags
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c_tags, c_hash = st.columns([2, 1])
    with c_tags:
        st.subheader("📊 25 TỪ KHÓA SEO")
        tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data.get('tags', [])])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.text_area("Copy bộ Tag:", ", ".join(data.get('tags', [])), height=80)
    with c_hash:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
        st.subheader("💬 GHIM BÌNH LUẬN")
        st.info(data.get('pinned', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # Công cụ Thumbnail
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🖼️ Ý TƯỞNG THIẾT KẾ THUMBNAIL")
    style = st.radio("Phong cách ảnh:", ["Ảnh Thật", "3D Render", "Điện Ảnh", "Hoạt Hình"], horizontal=True)
    if st.button("🎨 TẠO PROMPT VẼ ẢNH"):
        prompt_img = f"Tạo prompt vẽ ảnh Thumbnail cho tiêu đề '{sel_title}' phong cách {style}. Đưa ra các gợi ý về màu sắc, bố cục và chữ trên ảnh."
        img_res = get_ai_response(api_key, prompt_img)
        if img_res == "ERROR_QUOTA": st.error("⚠️ Hết hạn mức. Chờ 1 chút nhé!")
        else: st.write(img_res)
    st.markdown('</div>', unsafe_allow_html=True)
