import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN MẪU ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s; height: 3em; }
    
    /* Màu sắc nút bấm */
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

# --- 2. HÀM AI THÔNG MINH (CHỐNG LỖI 404 & 429) ---
def get_ai_response(api_key, prompt):
    genai.configure(api_key=api_key)
    # Fix cứng model 1.5-flash để đảm bảo tốc độ và không bị lỗi 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "ResourceExhausted" in err:
            return "ERROR_429"
        return f"LỖI: {err}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 CÀI ĐẶT API")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Hệ thống đã được dọn sạch code thừa và tối ưu tốc độ xử lý.")

# KHỐI 1: NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)")
        channel = st.text_input("Link kênh của bạn (Tùy chọn)")
    
    if st.button("🚀 TẠO NỘI DUNG TỐI ƯU", use_container_width=True):
        if kw and api_key:
            with st.spinner("Đang cào dữ liệu và phân tích SEO..."):
                prompt = f"""Bạn là chuyên gia SEO Youtube. Phân tích '{kw}' ({lang}). 
                Trả về JSON thuần túy (không kèm markdown ```json):
                {{
                    "titles": ["10 tiêu đề hay"],
                    "tags": ["25 tags"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "mẫu bình luận ghim",
                    "comment_rival": "Bình luận hay từ đối thủ gợi ý"
                }}"""
                res = get_ai_response(api_key, prompt)
                
                if res == "ERROR_429":
                    st.error("⚠️ Bạn đã dùng hết hạn mức API (Lỗi 429). Hãy đợi 60 giây rồi thử lại.")
                elif res.startswith("LỖI:"):
                    st.error(res)
                else:
                    try:
                        # Lọc lấy JSON an toàn
                        json_match = re.search(r'\{.*\}', res, re.DOTALL)
                        if json_match:
                            st.session_state.seo_data = json.loads(json_match.group())
                            st.session_state.kw = kw
                        else: 
                            st.error("AI không trả về đúng định dạng. Hãy thử bấm lại nút.")
                    except: 
                        st.error("Lỗi phân tích dữ liệu (Parse Error). AI phản hồi sai định dạng.")
        else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: HIỂN THỊ KẾT QUẢ
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Nút công cụ mở rộng
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1: 
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        st.button("🔍 Kiểm tra danh mục")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_btn2: 
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        st.button("🏷️ Thẻ tag video")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_btn3: 
        st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
        st.button("ℹ️ Thông tin video")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2.1 Tiêu đề & Tạo mô tả
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    # Sử dụng .get() để tránh lỗi nếu JSON trả về thiếu key
    for i, t in enumerate(data.get('titles', []), 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    selected_title = st.selectbox("Chọn 1 tiêu đề để AI viết mô tả chi tiết:", data.get('titles', []))
    
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("AI đang soạn thảo mô tả chuẩn SEO..."):
            desc_prompt = f"Viết mô tả Youtube chuẩn SEO cho tiêu đề: '{selected_title}'. Bao gồm: Giới thiệu, Nội dung chính, Hashtags và Kêu gọi hành động."
            desc_res = get_ai_response(api_key, desc_prompt)
            
            if desc_res == "ERROR_429":
                st.error("⚠️ Quá tải API! Vui lòng đợi vài giây rồi thử lại.")
            else:
                st.session_state.generated_desc = desc_res
    
    if 'generated_desc' in st.session_state:
        st.markdown('<div class="desc-output">', unsafe_allow_html=True)
        st.write(st.session_state.generated_desc)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.2 Tags & Hashtags & Bình luận
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c_a, c_b = st.columns([2, 1])
    with c_a:
        st.subheader("📊 25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO")
        tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data.get('tags', [])])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.text_area("Copy bộ Tag:", ", ".join(data.get('tags', [])), height=100)
    with c_b:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
        st.subheader("💬 BÌNH LUẬN MẪU")
        st.info(data.get('pinned', ''))
        st.subheader("📌 BÌNH LUẬN ĐỐI THỦ")
        st.caption(data.get('comment_rival', 'Đang cập nhật...'))
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.3 Công cụ tạo Prompt ảnh (Tích hợp thông minh hơn)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO PROMPT ẢNH THUMBNAIL (NANO BANANA 2)")
    t_text = st.text_input("Văn bản muốn hiện trên ảnh", placeholder="Ví dụ: KIẾM 1000$ MỖI THÁNG")
    style = st.selectbox("Phong cách ảnh", ["Realistic Photorealistic", "3D Disney Style", "Cyberpunk", "Minimalist"])
    
    if st.button("🖼️ TẠO MÃ PROMPT VẼ ẢNH"):
        with st.spinner("Đang kết xuất Prompt chuyên nghiệp..."):
            img_prompt = f"Youtube Thumbnail for '{selected_title}'. Art style: {style}. Bold focal text reading: '{t_text}'. High contrast, 8k resolution, cinematic lighting, eye-catching composition."
            st.success("Copy mã dưới đây dán vào các công cụ AI vẽ ảnh (như Gemini 3 Flash Image / Nano Banana 2):")
            st.code(img_prompt, language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)
