import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN MẪU GỐC ---
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
    
    /* Màu sắc nút bấm chuẩn theo ảnh 844 */
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
    # Tự động chọn model khả dụng nhất trong tài khoản của bạn (Gemini 3 hoặc 1.5)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LỖI: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 CÀI ĐẶT API")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Hệ thống đã sửa lỗi định dạng AI và tối ưu giao diện mẫu.")

# KHỐI 1: NHẬP LIỆU (Theo mẫu ảnh 843)
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
            with st.spinner("Đang phân tích dữ liệu SEO..."):
                prompt = f"""Bạn là chuyên gia SEO Youtube. Phân tích '{kw}' ({lang}). 
                Trả về JSON thuần túy (không kèm lời dẫn):
                {{
                    "titles": ["10 tiêu đề hay"],
                    "tags": ["25 tags"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "mẫu bình luận ghim",
                    "comment_rival": "Bình luận hay từ đối thủ gợi ý"
                }}"""
                res = get_ai_response(api_key, prompt)
                try:
                    # Lọc lấy JSON từ phản hồi AI để tránh lỗi định dạng
                    json_match = re.search(r'\{.*\}', res, re.DOTALL)
                    if json_match:
                        st.session_state.seo_data = json.loads(json_match.group())
                        st.session_state.kw = kw
                    else: st.error("AI không trả về đúng định dạng JSON. Hãy thử lại.")
                except: st.error("Lỗi phân tích dữ liệu AI.")
        else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: HIỂN THỊ KẾT QUẢ (Theo mẫu ảnh 844, 845, 846)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Nút công cụ mở rộng (Ảnh 844)
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with col_btn2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_btn3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # 2.1 Tiêu đề & Tạo mô tả (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    for i, t in enumerate(data['titles'], 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    # Chức năng chọn tiêu đề để viết mô tả (Mở rộng)
    selected_title = st.selectbox("Chọn 1 tiêu đề để AI viết mô tả chi tiết:", data['titles'])
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("AI đang soạn thảo mô tả chuẩn SEO..."):
            desc_prompt = f"Viết mô tả Youtube chuẩn SEO cho tiêu đề: '{selected_title}'. Bao gồm: Giới thiệu, Nội dung chính, Hashtags và Kêu gọi hành động."
            st.session_state.generated_desc = get_ai_response(api_key, desc_prompt)
    
    if 'generated_desc' in st.session_state:
        st.markdown('<div class="desc-output">', unsafe_allow_html=True)
        st.write(st.session_state.generated_desc)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.2 Tags & Hashtags & Bình luận (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c_a, c_b = st.columns([2, 1])
    with c_a:
        st.subheader("📊 25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO")
        tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.text_area("Copy bộ Tag:", ", ".join(data['tags']), height=100)
    with c_b:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data['hashtags']))
        st.subheader("💬 BÌNH LUẬN MẪU")
        st.info(data['pinned'])
        st.subheader("📌 BÌNH LUẬN ĐỐI THỦ")
        st.caption(data.get('comment_rival', 'Đang cập nhật...'))
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.3 Công cụ tạo Prompt ảnh (Ảnh 847)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO PROMPT ẢNH THUMBNAIL")
    t_text = st.text_input("Văn bản muốn hiện trên ảnh", placeholder="Ví dụ: KIẾM 1000$ MỖI THÁNG")
    style = st.selectbox("Phong cách ảnh", ["Realistic Photorealistic", "3D Disney Style", "Cyberpunk", "Minimalist"])
    
    if st.button("🖼️ TẠO MÃ PROMPT"):
        img_prompt = f"Youtube Thumbnail for '{selected_title}', style: {style}, focal text: '{t_text}', high contrast, 8k resolution, cinematic lighting."
        st.code(img_prompt, language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)
