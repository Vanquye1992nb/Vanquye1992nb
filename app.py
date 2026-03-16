import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN (Dựa trên ảnh 843, 844, 847) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .main-title { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em; }
    .btn-orange button { background: #ff4b2b !important; color: white !important; border: none !important; }
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    .desc-box { background: #0f172a; padding: 20px; border-radius: 10px; border: 1px dashed #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG GỌI AI THÔNG MINH (FIX LỖI 404 & 429) ---
def call_ai_smart(api_key, prompt, is_json=True):
    genai.configure(api_key=api_key)
    # Sử dụng model gemini-1.5-flash là phiên bản ổn định nhất hiện nay
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        if is_json:
            # Dùng Regex để tách lấy phần JSON chính xác
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group()) if match else None
        return text
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "ResourceExhausted" in err_msg:
            return "ERROR_QUOTA"
        return f"ERROR: {err_msg}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-title">🚀 HỆ THỐNG SEO VIDEO AI</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Lưu ý: Nếu dùng bản miễn phí, hãy đợi 60 giây giữa các lần nhấn nút.")

# KHỐI NHẬP LIỆU (Dựa trên ảnh 843)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)", value="sách")
        channel = st.text_input("Tên kênh của bạn")
    
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", type="primary"):
        if kw and api_key:
            with st.spinner("AI đang phân tích dữ liệu SEO..."):
                prompt = f"Phân tích SEO cho từ khóa '{kw}' ({lang}). Trả về JSON: {{'titles': [], 'tags': [], 'hashtags': [], 'pinned': ''}}"
                data = call_ai_smart(api_key, prompt)
                
                if data == "ERROR_QUOTA":
                    st.error("⚠️ Bạn đã dùng hết hạn mức API miễn phí (Lỗi 429). Hãy đợi 1 phút.")
                elif isinstance(data, dict):
                    st.session_state.seo_data = data
                    st.session_state.kw = kw
                else: st.error(f"Lỗi: {data}")
        else: st.warning("Vui lòng nhập API Key và Từ khóa.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI HIỂN THỊ KẾT QUẢ (Dựa trên ảnh 844, 845, 846, 847, 9d3f5f)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # 3 Nút chức năng phụ (Ảnh 844)
    st.markdown(f'<h3 style="text-align:center;">KẾT QUẢ CHO: {st.session_state.kw.upper()}</h3>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.button("🔍 Kiểm tra danh mục")
    with col_b: st.button("🏷️ Thẻ tag video")
    with col_c: st.button("ℹ️ Thông tin video")

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    for i, t in enumerate(data.get('titles', []), 1):
        st.write(f"**Tiêu đề {i}:** {t}")
    
    st.divider()
    sel_title = st.selectbox("Chọn tiêu đề để viết mô tả:", data.get('titles', []))
    
    # Nút màu cam tạo mô tả
    st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
    if st.button("📝 TẠO MÔ TẢ CHO TIÊU ĐỀ ĐÃ CHỌN"):
        with st.spinner("Đang soạn mô tả SEO..."):
            prompt_desc = f"Viết mô tả Youtube chuẩn SEO cho: {sel_title}. Bao gồm lời chào, nội dung chính và kêu gọi hành động."
            desc = call_ai_smart(api_key, prompt_desc, is_json=False)
            if desc == "ERROR_QUOTA": st.error("⚠️ Hạn mức API đã hết. Hãy đợi 60 giây.")
            else: st.session_state.final_desc = desc
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'final_desc' in st.session_state:
        st.markdown(f'<div class="desc-box">{st.session_state.final_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tags & Hashtags (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 25 TỪ KHÓA SEO TỐI ƯU")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    c_h, c_p = st.columns(2)
    with c_h:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
    with c_p:
        st.subheader("💬 BÌNH LUẬN GHIM")
        st.info(data.get('pinned', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # Thiết kế Thumbnail (Dựa trên ảnh 847, 9d3f5f)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🖼️ THIẾT KẾ HÌNH ẢNH THU NHỎ")
    style = st.radio("Chọn phong cách Thumbnail:", ["Ảnh Thật", "3D Render", "Điện Ảnh", "Hoạt Hình", "Tối Giản"], horizontal=True)
    
    if st.button("🎨 TẠO Ý TƯỞNG THUMBNAIL (NANO BANANA 2)"):
        with st.spinner("AI đang lên ý tưởng hình ảnh..."):
            prompt_thumb = f"Đưa ra ý tưởng thiết kế Thumbnail Youtube cho video '{sel_title}' theo phong cách {style}. Đề xuất màu sắc, bố cục và chữ trên ảnh."
            thumb_res = call_ai_smart(api_key, prompt_thumb, is_json=False)
            if thumb_res == "ERROR_QUOTA": st.error("⚠️ Hãy đợi 1 phút trước khi tiếp tục.")
            else: st.write(thumb_res)
    st.markdown('</div>', unsafe_allow_html=True)
