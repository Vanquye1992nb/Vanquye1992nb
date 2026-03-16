import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN (THEO MẪU ẢNH 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em; }
    
    /* Màu nút bấm chuẩn ảnh 844 */
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    .desc-output { background: #0f172a; padding: 15px; border-radius: 10px; border-left: 5px solid #f1c40f; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM GỌI AI SIÊU CẤP (CHỐNG LỖI 429 & 404) ---
def call_gemini_safe(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        # Sửa lỗi 404: Sử dụng tên model chính thức
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Cơ chế tự động thử lại nếu bị nghẽn (429)
        for i in range(3): 
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    time.sleep(2 * (i + 1)) # Chờ 2, 4, 6 giây
                    continue
                raise e
        return "ERROR_QUOTA"
    except Exception as e:
        return f"LỖI HỆ THỐNG: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 CÀI ĐẶT")
    api_key = st.text_input("Nhập Gemini API Key", type="password")
    st.warning("Lưu ý: Nếu dùng bản miễn phí, không nên nhấn nút quá liên tục.")

# KHỐI 1: NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: cách làm bánh flan")
        channel = st.text_input("Link kênh của bạn")
    
    if st.button("🚀 TẠO NỘI DUNG TỐI ƯU", use_container_width=True):
        if not api_key or not kw:
            st.error("Vui lòng nhập đầy đủ API Key và Từ khóa!")
        else:
            with st.spinner("Đang phân tích SEO..."):
                prompt = f"""Bạn là chuyên gia SEO Youtube. Hãy phân tích '{kw}' ({lang}). 
                Trả về JSON thuần túy (không kèm markdown ```json):
                {{
                    "titles": ["10 tiêu đề hay"],
                    "tags": ["25 tags"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "Bình luận ghim",
                    "comment_rival": "Bình luận đối thủ"
                }}"""
                res = call_gemini_safe(api_key, prompt)
                
                if res == "ERROR_QUOTA":
                    st.error("⚠️ Bạn đã hết hạn mức API trong phút này. Hãy chờ 30-60 giây.")
                elif "LỖI" in res:
                    st.error(res)
                else:
                    try:
                        # Làm sạch chuỗi trước khi parse JSON
                        clean_json = re.search(r'\{.*\}', res, re.DOTALL).group()
                        st.session_state.seo_data = json.loads(clean_json)
                        st.session_state.kw_display = kw
                    except:
                        st.error("AI trả về dữ liệu lỗi định dạng. Hãy thử lại.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: HIỂN THỊ KẾT QUẢ
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # Nút công cụ
    cb1, cb2, cb3 = st.columns(3)
    with cb1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with cb2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with cb3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # Tiêu đề & Mô tả
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🏅 KẾT QUẢ CHO: {st.session_state.kw_display.upper()}")
    
    titles = data.get('titles', [])
    for i, t in enumerate(titles, 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    sel_title = st.selectbox("Chọn tiêu đề để viết mô tả:", titles if titles else ["Chưa có dữ liệu"])
    if st.button("📝 VIẾT MÔ TẢ CHI TIẾT"):
        with st.spinner("Đang soạn mô tả..."):
            desc_prompt = f"Viết mô tả Youtube SEO dài cho tiêu đề: {sel_title}. Gồm Intro, Nội dung, Hashtag."
            desc_res = call_gemini_safe(api_key, desc_prompt)
            st.session_state.generated_desc = desc_res
            
    if 'generated_desc' in st.session_state:
        st.markdown(f'<div class="desc-output">{st.session_state.generated_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tags & Hashtags
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📊 25 TỪ KHÓA SEO")
        tags = data.get('tags', [])
        st.markdown("".join([f'<span class="tag-chip">{tag}</span>' for tag in tags]), unsafe_allow_html=True)
        st.text_area("Bộ thẻ tag (Copy):", ", ".join(tags), height=100)
    with col_r:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
        st.subheader("💬 BÌNH LUẬN GHIM")
        st.info(data.get('pinned', 'Trống'))
    st.markdown('</div>', unsafe_allow_html=True)

    # Thumbnail Tool
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 Ý TƯỞNG THUMBNAIL")
    t_txt = st.text_input("Văn bản trên ảnh", value="BÍ MẬT ĐƯỢC TIẾT LỘ")
    if st.button("🖼️ TẠO PROMPT ẢNH"):
        prompt_img = f"Tạo prompt vẽ ảnh thumbnail Youtube cho tiêu đề '{sel_title}' với chữ '{t_txt}', phong cách điện ảnh."
        st.code(call_gemini_safe(api_key, prompt_img))
    st.markdown('</div>', unsafe_allow_html=True)
