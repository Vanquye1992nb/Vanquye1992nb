import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN TOOL SEO (Ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }
    .stButton>button { 
        border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .btn-blue { background: #2563eb !important; color: white !important; }
    .btn-green { background: #10b981 !important; color: white !important; }
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG AI TỰ ĐỘNG DÒ MODEL (CHỐNG LỖI 404) ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for p in ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']:
            if p in models: return genai.GenerativeModel(p)
        return genai.GenerativeModel(models[0])
    except: return None

# --- 3. LOGIC XỬ LÝ DỮ LIỆU ---
def analyze_seo(api_key, keyword, lang, ref):
    model = get_model(api_key)
    prompt = f"""
    Bạn là chuyên gia SEO Youtube. Phân tích '{keyword}' ({lang}). Link đối thủ: {ref}.
    Trả về JSON:
    {{
        "titles": ["10 tiêu đề hấp dẫn"],
        "tags": ["25 tags SEO"],
        "hashtags": ["10 hashtag thịnh hành"],
        "pinned_comment": "Bình luận ghim mẫu thu hút tương tác",
        "competitor_analysis": "Phân tích nhanh đối thủ"
    }}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(re.search(r'\{.*\}', response.text, re.DOTALL).group())
    except: return None

def generate_desc(api_key, title):
    model = get_model(api_key)
    prompt = f"Viết mô tả Youtube chuẩn SEO, đầy đủ từ khóa và kêu gọi hành động cho tiêu đề: '{title}'"
    return model.generate_content(prompt).text

# --- 4. GIAO DIỆN CHÍNH (TẤT CẢ TRÊN 1 TRANG) ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cài đặt")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Hệ thống tự động đồng bộ hóa dữ liệu trên cùng một trang.")

# KHỐI 1: NHẬP LIỆU (Ảnh 843)
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
            with st.spinner("Đang phân tích dữ liệu..."):
                st.session_state.seo_data = analyze_seo(api_key, kw, lang, ref)
                st.session_state.kw = kw
        else: st.warning("Vui lòng điền đủ thông tin!")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: KẾT QUẢ & CÔNG CỤ MỞ RỘNG (Ảnh 844, 845, 846)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # 2.1 Tiêu đề & Viết mô tả theo tiêu đề (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    selected_title = st.selectbox("Bạn muốn viết mô tả SEO cho tiêu đề nào?", data['titles'])
    
    if st.button("📝 TẠO MÔ TẢ CHO TIÊU ĐỀ ĐÃ CHỌN", type="primary"):
        with st.spinner("AI đang viết mô tả..."):
            st.session_state.desc = generate_desc(api_key, selected_title)
    
    if 'desc' in st.session_state:
        st.text_area("Nội dung mô tả SEO:", st.session_state.desc, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.2 Tags & Hashtags & Bình luận (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("📊 25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO")
        tags_html = "".join([f'<span class="tag-chip">{t}</span>' for t in data['tags']])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.text_area("Copy Tags:", ", ".join(data['tags']))
    with col_b:
        st.subheader("#️⃣ HASHTAGS")
        st.code("\n".join(data['hashtags']))
        st.subheader("💬 BÌNH LUẬN GHIM")
        st.info(data['pinned_comment'])
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.3 Công cụ tạo Prompt ảnh (Ảnh 847)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO ẢNH MINH HỌA")
    thumb_text = st.text_input("Văn bản trên Thumbnail (Tùy chọn)", placeholder="Ví dụ: BÍ MẬT ĐƯỢC TIẾT LỘ")
    style = st.radio("Chọn phong cách Thumbnail", ["Ảnh thật", "3D Render", "Điện ảnh", "Hoạt hình"], horizontal=True)
    
    if st.button("🖼️ TẠO PROMPT ẢNH"):
        prompt_ai = f"High-quality Youtube Thumbnail for '{selected_title}', style {style}, text focus: '{thumb_text}', 8k resolution, vibrant colors."
        st.code(prompt_ai, language="markdown")
    
    st.divider()
    c_down, c_new = st.columns(2)
    c_down.button("📥 Tải về toàn bộ nội dung", use_container_width=True)
    if c_new.button("🔄 Tạo nội dung mới", use_container_width=True):
        del st.session_state.seo_data
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
