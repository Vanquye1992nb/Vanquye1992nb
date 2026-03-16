import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN MẪU (Ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s; height: 3.5em; }
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    .desc-box { background: #0f172a; padding: 20px; border-radius: 10px; border: 1px dashed #f1c40f; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM GỌI AI AN TOÀN (FIX LỖI ĐỊNH DẠNG) ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = 'models/gemini-1.5-flash'
        return genai.GenerativeModel(target if target in models else models[0])
    except: return None

def clean_json_response(text):
    """Lọc lấy đúng phần JSON để tránh lỗi phân tích dữ liệu"""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except: return None

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cài đặt")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Hệ thống đã tách luồng dữ liệu để chống lỗi 429 và lỗi định dạng.")

# KHỐI 1: NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)")
        channel = st.text_input("Link kênh của bạn")
    
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH SEO", type="primary"):
        if kw and api_key:
            with st.spinner("AI đang xử lý dữ liệu JSON..."):
                model = get_model(api_key)
                prompt = f"""Bạn là chuyên gia SEO. Phân tích '{kw}' ({lang}). Link đối thủ: {ref}.
                Trả về DUY NHẤT mã JSON (không kèm lời dẫn):
                {{
                    "titles": ["10 tiêu đề"], "tags": ["25 tags"], "hashtags": ["10 hashtags"],
                    "pinned": "Mẫu bình luận ghim", "competitor": "Phân tích đối thủ ngắn"
                }}"""
                response = model.generate_content(prompt)
                data = clean_json_response(response.text)
                if data:
                    st.session_state.seo_data = data
                    st.session_state.kw = kw
                else: st.error("Lỗi: AI không trả về đúng cấu trúc JSON. Hãy thử lại!")
        else: st.warning("Hãy nhập API Key và Từ khóa.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: HIỂN THỊ & MỞ RỘNG
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Nút bấm công cụ
    col_a, col_b = st.columns(2)
    with col_a: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)

    # 2.1 Tiêu đề & Tạo mô tả (FIX LỖI ĐỊNH DẠNG TẠI ĐÂY)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE TỐI ƯU")
    for i, t in enumerate(data['titles'], 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    selected_title = st.selectbox("Chọn tiêu đề bạn muốn AI viết mô tả chi tiết:", data['titles'])
    
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("AI đang viết văn bản mô tả..."):
            model = get_model(api_key)
            # Yêu cầu trả về văn bản thường, không phải JSON để tránh lỗi parse
            prompt_desc = f"Viết mô tả Youtube chuẩn SEO cho tiêu đề: '{selected_title}'. Có lời chào, nội dung chính, kêu gọi đăng ký và hashtags."
            res_desc = model.generate_content(prompt_desc)
            st.session_state.final_desc = res_desc.text

    if 'final_desc' in st.session_state:
        st.markdown('**Kết quả mô tả chi tiết:**')
        st.markdown(f'<div class="desc-box">{st.session_state.final_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.2 Tags & Hashtags
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 25 TỪ KHÓA CHUẨN SEO")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.text_area("Copy Tags:", ", ".join(data['tags']))
    
    c_h, c_p = st.columns(2)
    with c_h:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data['hashtags']))
    with c_p:
        st.subheader("💬 BÌNH LUẬN GHIM")
        st.info(data['pinned'])
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.3 Prompt Ảnh
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO PROMPT ẢNH THUMBNAIL")
    t_text = st.text_input("Chữ hiện trên ảnh", value="BÍ MẬT SEO")
    if st.button("✨ TẠO MÃ PROMPT"):
        st.code(f"Youtube Thumbnail for video '{selected_title}', style cinematic, text: '{t_text}', 8k resolution.", language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)
