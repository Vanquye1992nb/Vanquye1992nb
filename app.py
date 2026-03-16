import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN (Dựa trên ảnh 843, 844, 847) ---
st.set_page_config(page_title="Hệ Thống SEO AI Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .main-title { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em; }
    /* Nút màu cam đặc trưng cho phần tạo mô tả */
    .btn-orange button { background: #ff4b2b !important; color: white !important; border: none !important; }
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG GỌI AI AN TOÀN ---
def call_ai_safe(api_key, prompt, is_json=True):
    genai.configure(api_key=api_key)
    # Sử dụng model 1.5 flash ổn định nhất hiện nay
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        if is_json:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group()) if match else None
        return text
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "ERROR_QUOTA"
        return f"ERROR: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-title">🚀 HỆ THỐNG SEO VIDEO AI</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Sử dụng model Gemini 1.5 Flash để tránh lỗi 404.")

# KHỐI NHẬP LIỆU (Ảnh 843)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)")
        channel = st.text_input("Tên kênh của bạn")
    
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", type="primary"):
        if kw and api_key:
            with st.spinner("AI đang xử lý dữ liệu..."):
                prompt = f"Phân tích SEO cho từ khóa '{kw}' ({lang}). Trả về JSON: {{'titles': [], 'tags': [], 'hashtags': [], 'pinned': ''}}"
                data = call_ai_safe(api_key, prompt)
                
                if data == "ERROR_QUOTA":
                    st.error("⚠️ Hết hạn mức API. Hãy đợi 60 giây rồi thử lại.")
                elif isinstance(data, dict):
                    st.session_state.seo_data = data
                    st.session_state.kw = kw
                else: st.error(f"Lỗi: {data}")
        else: st.warning("Vui lòng điền đủ thông tin.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI HIỂN THỊ KẾT QUẢ (Ảnh 844, 845, 846, 847)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Tiêu đề (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    for i, t in enumerate(data['titles'], 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    sel_title = st.selectbox("Chọn tiêu đề để viết mô tả:", data['titles'])
    
    # Nút màu cam tạo mô tả
    st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
    if st.button("📝 TẠO MÔ TẢ CHO TIÊU ĐỀ ĐÃ CHỌN"):
        with st.spinner("Đang soạn mô tả..."):
            prompt_desc = f"Viết mô tả Youtube chuẩn SEO cho: {sel_title}"
            desc = call_ai_safe(api_key, prompt_desc, is_json=False)
            if desc == "ERROR_QUOTA": st.error("⚠️ Đợi 60 giây để dùng tiếp.")
            else: st.session_state.final_desc = desc
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'final_desc' in st.session_state:
        st.text_area("Kết quả mô tả:", st.session_state.final_desc, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tags & Hashtags (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 25 TỪ KHÓA TỐI ƯU SEO")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tích hợp Prompt Thumbnail (Ảnh 847, image_9d3f5f)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO PROMPT THUMBNAIL")
    t_text = st.text_input("Văn bản trên ảnh", value="BÍ MẬT SEO")
    if st.button("✨ TẠO PROMPT CHO NANO BANANA 2"):
        with st.spinner("AI đang thiết kế prompt..."):
            prompt_thumb = f"Tạo prompt vẽ ảnh Thumbnail Youtube cho video '{sel_title}' với chữ '{t_text}'. Phong cách cinematic, 8k."
            thumb_res = call_ai_safe(api_key, prompt_thumb, is_json=False)
            st.code(thumb_res, language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)
