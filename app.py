import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- CẤU HÌNH GIAO DIỆN CHUẨN MẪU GỐC ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube Văn Quyết", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .main-container { max-width: 900px; margin: auto; }
    .glass-card { 
        background: #2d333b; padding: 25px; 
        border-radius: 12px; border: 1px solid #444c56; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 26px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; transition: 0.3s; }
    /* Màu nút bấm chuẩn ảnh mẫu */
    div[data-testid="stHorizontalBlock"] button { height: 45px; }
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    .btn-orange button { background: #ea580c !important; color: white !important; }
    
    .tag-chip { 
        background: #444c56; color: #adb5bd; padding: 6px 12px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #57606a; font-size: 14px;
    }
    .desc-box { background: #1c2128; border-left: 5px solid #2563eb; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- XỬ LÝ AI ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def safe_generate(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "LỖI: Bạn đã hết hạn mức sử dụng API miễn phí. Vui lòng thử lại sau 1 phút hoặc đổi API Key mới."
        return f"Lỗi hệ thống: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Gemini API Key", type="password", help="Lấy tại Google AI Studio")
    if not api_key:
        st.warning("Vui lòng nhập API Key để bắt đầu.")

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# PHẦN 1: NHẬP LIỆU (Ảnh 843)
st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #94a3b8;">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm bánh flan")
        channel = st.text_input("Link kênh của bạn (Tùy chọn)")
    
    if st.button("🚀 Tạo Nội Dung Tối Ưu", type="primary"):
        if kw and api_key:
            with st.spinner("AI đang phân tích đối thủ và tối ưu hóa..."):
                model = get_model(api_key)
                prompt = f"""Bạn là một chuyên gia SEO Youtube. Hãy phân tích từ khóa '{kw}' và link tham khảo '{ref}'.
                Trả về kết quả dạng JSON với các trường: titles (mảng 10 cái), tags (mảng 25 cái), hashtags (mảng 10 cái), pinned_comment. 
                Ngôn ngữ: {lang}."""
                res_text = safe_generate(model, prompt)
                if "LỖI" in res_text:
                    st.error(res_text)
                else:
                    try:
                        data = json.loads(re.search(r'\{.*\}', res_text, re.DOTALL).group())
                        st.session_state.seo_res = data
                        st.session_state.kw_analyzed = kw
                    except: st.error("Lỗi định dạng dữ liệu AI. Hãy thử lại.")
        else: st.error("Hãy điền từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# PHẦN 2: KẾT QUẢ (Ảnh 844, 846)
if 'seo_res' in st.session_state:
    data = st.session_state.seo_res
    
    st.markdown(f'<h2 style="color:white; text-align:center;">KẾT QUẢ TỐI ƯU CHO TỪ KHÓA: <span style="color:#f1c40f;">{st.session_state.kw_analyzed.upper()}</span></h2>', unsafe_allow_html=True)
    
    # Nút bấm công cụ đối thủ (Ảnh 844)
    st.markdown('<p style="text-align:center;">🚀 CÔNG CỤ PHÂN TÍCH ĐỐI THỦ:</p>', unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("Kiểm tra danh mục video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_btn2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("Kiểm tra thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_btn3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # Tiêu đề (Ảnh 844, 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h4>🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN</h4>', unsafe_allow_html=True)
    for i, t in enumerate(data['titles'], 1):
        st.info(f"**Tiêu đề {i}:** {t}")
    
    st.divider()
    # CHỨC NĂNG TÌM KIẾM MÔ TẢ THEO TIÊU ĐỀ (Sửa lỗi ảnh 867)
    st.markdown('<p style="text-align:center;">Bạn muốn viết mô tả YouTube chuẩn SEO cho tiêu đề nào?</p>', unsafe_allow_html=True)
    selected_title = st.selectbox("Chọn tiêu đề để tạo mô tả:", data['titles'])
    
    if st.button("📝 TẠO MÔ TẢ CHO TIÊU ĐỀ ĐÃ CHỌN"):
        with st.spinner("Đang tạo mô tả..."):
            model = get_model(api_key)
            desc_prompt = f"Viết một đoạn mô tả video Youtube chuẩn SEO cho tiêu đề: '{selected_title}'. Có bao gồm kêu gọi đăng ký kênh."
            desc_res = safe_generate(model, desc_prompt)
            st.session_state.final_desc = desc_res
            
    if 'final_desc' in st.session_state:
        st.markdown('<div class="desc-box">', unsafe_allow_html=True)
        st.write(st.session_state.final_desc)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Từ khóa (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.divider()
    st.subheader("#️⃣ HASHTAGS SEO")
    st.code(" ".join(data['hashtags']))
    st.subheader("💬 BÌNH LUẬN GHIM MẪU")
    st.info(data['pinned_comment'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Prompt Ảnh (Ảnh 847)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO ẢNH MINH HỌA")
    txt_thumb = st.text_input("Văn bản trên Thumbnail (Tùy chọn)", placeholder="Ví dụ: BÍ MẬT")
    style = st.radio("Chọn phong cách", ["Ảnh thật", "3D Render", "Điện ảnh", "Hoạt hình"], horizontal=True)
    
    if st.button("✨ Tạo Prompt Ảnh", type="secondary"):
        st.code(f"High-quality Youtube Thumbnail for '{selected_title}', {style} style, text: '{txt_thumb}', cinematic lighting, 8k", language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
