import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (Giống mẫu ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: #2d333b; padding: 25px; 
        border-radius: 12px; border: 1px solid #444c56; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; }
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    .tag-chip { 
        background: #444c56; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #57606a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM XỬ LÝ AI AN TOÀN ---
def call_gemini_ai(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "ResourceExhausted" in str(e) or "429" in str(e):
            return "ERROR_QUOTA: Bạn đã hết lượt dùng API miễn phí trong phút này. Hãy đợi 60s."
        return f"ERROR_SYSTEM: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 Chuyên Gia SEO Video AI</p>', unsafe_allow_html=True)

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Phiên bản sửa lỗi định dạng JSON & Quota API.")

# FORM NHẬP LIỆU (Ảnh 843)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính")
    
    if st.button("Tạo Nội Dung Tối Ưu", type="primary"):
        if kw and api_key:
            # Prompt ép JSON cực mạnh để tránh lỗi định dạng
            prompt = f"""Bạn là chuyên gia SEO. Phân tích '{kw}'. Link tham khảo: '{ref}'.
            Trả về CHỈ DUY NHẤT mã JSON theo mẫu này, không nói thêm:
            {{
                "titles": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"],
                "tags": ["tag1", "tag2", "tag3"],
                "hashtags": ["#h1", "#h2"],
                "pinned": "nội dung bình luận ghim"
            }}
            Ngôn ngữ: {lang}."""
            
            with st.spinner("Đang phân tích..."):
                res = call_gemini_ai(api_key, prompt)
                if "ERROR" in res:
                    st.error(res)
                else:
                    try:
                        # Dùng Regex để tách đúng khối JSON nếu AI có nói lảm nhảm bên ngoài
                        json_str = re.search(r'\{.*\}', res, re.DOTALL).group()
                        st.session_state.data = json.loads(json_str)
                        st.session_state.kw = kw
                    except:
                        st.error("Lỗi định dạng AI: Phản hồi không phải JSON hợp lệ. Hãy thử lại.")
        else:
            st.warning("Vui lòng nhập API Key và Từ khóa.")
    st.markdown('</div>', unsafe_allow_html=True)

# HIỂN THỊ KẾT QUẢ (Ảnh 844, 845, 846)
if 'data' in st.session_state:
    data = st.session_state.data
    
    st.markdown(f"### KẾT QUẢ CHO: {st.session_state.kw}")
    
    # Nút bấm công cụ (Ảnh 844)
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ HẤP DẪN")
    for i, t in enumerate(data['titles'], 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    sel_title = st.selectbox("Chọn tiêu đề để AI viết mô tả:", data['titles'])
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("AI đang viết mô tả chuẩn SEO..."):
            desc_prompt = f"Viết mô tả Youtube chuẩn SEO cho video: '{sel_title}'. Có kêu gọi hành động."
            st.session_state.desc_result = call_gemini_ai(api_key, desc_prompt)
    
    if 'desc_result' in st.session_state:
        st.text_area("Mô tả của bạn:", st.session_state.desc_result, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tag & Hashtag (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 25 TỪ KHÓA TÌM KIẾM CAO")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.subheader("#️⃣ HASHTAGS")
    st.code(" ".join(data['hashtags']))
    st.markdown('</div>', unsafe_allow_html=True)
