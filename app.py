import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN MẪU (Ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s; }
    /* Màu nút bấm chuẩn ảnh mẫu 844 */
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    .btn-orange button { background: #f97316 !important; color: white !important; border: none !important; }
    
    .tag-chip { 
        background: #334155; color: #60a5fa; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569;
    }
    .desc-box { background: #0f172a; padding: 20px; border-radius: 10px; border: 1px dashed #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM AI XỬ LÝ LỖI HẠN MỨC (FIX LỖI 867) ---
def call_gemini_safe(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "ERROR_QUOTA" # Trả về mã lỗi để xử lý giao diện
        return f"ERROR: {str(e)}"

# --- 3. LOGIC PHÂN TÍCH ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    # Sử dụng Gemini 3 Flash theo tài liệu mới nhất
    return genai.GenerativeModel('gemini-3-flash')

# --- 4. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cài đặt")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Phiên bản hỗ trợ Gemini 3 Flash mới nhất.")

# KHỐI NHẬP LIỆU (Ảnh 843)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)")
        channel = st.text_input("Link kênh của bạn")
    
    if st.button("🚀 TẠO NỘI DUNG TỐI ƯU", use_container_width=True):
        if kw and api_key:
            with st.spinner("AI đang phân tích dữ liệu SEO..."):
                model = get_model(api_key)
                prompt = f"""Bạn là chuyên gia SEO Youtube. Phân tích '{kw}' ({lang}).
                Trả về JSON thuần: {{ "titles": ["10 tiêu đề"], "tags": ["25 tags"], "hashtags": ["10 hashtags"], "pinned": "Bình luận ghim" }}"""
                res = call_gemini_safe(model, prompt)
                
                if res == "ERROR_QUOTA":
                    st.error("⚠️ Bạn đã hết hạn mức API miễn phí. Vui lòng đợi 1 phút rồi thử lại.")
                elif "ERROR" in res:
                    st.error(res)
                else:
                    try:
                        data = json.loads(re.search(r'\{.*\}', res, re.DOTALL).group())
                        st.session_state.seo_data = data
                        st.session_state.kw = kw
                    except: st.error("Lỗi định dạng AI. Hãy nhấn nút Tạo lại.")
        else: st.warning("Vui lòng điền đủ thông tin!")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI KẾT QUẢ (Ảnh 844, 845, 846)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # 3 Nút công cụ (Ảnh 844)
    st.markdown(f'<h3 style="text-align:center;">KẾT QUẢ CHO: {st.session_state.kw.upper()}</h3>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ YOUTUBE HẤP DẪN")
    for i, t in enumerate(data['titles'], 1):
        st.write(f"**Tiêu đề {i}:** {t}")
    
    st.divider()
    # PHẦN VIẾT MÔ TẢ (Sửa lỗi dứt điểm)
    selected_title = st.selectbox("Bạn muốn viết mô tả SEO cho tiêu đề nào?", data['titles'])
    
    # Nút màu cam chuẩn mẫu ảnh 867
    st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
    if st.button("📝 TẠO MÔ TẢ CHO TIÊU ĐỀ ĐÃ CHỌN"):
        with st.spinner("Đang viết mô tả chi tiết..."):
            model = get_model(api_key)
            # Tách luồng: Viết mô tả trả về text thường, không ép JSON để tránh lỗi parse
            prompt_desc = f"Viết mô tả Youtube chuẩn SEO, hấp dẫn cho video có tiêu đề: '{selected_title}'. Có kêu gọi hành động và hashtag."
            res_desc = call_gemini_safe(model, prompt_desc)
            
            if res_desc == "ERROR_QUOTA":
                st.error("⚠️ Hết hạn mức API. Hãy đợi 60 giây.")
            else:
                st.session_state.final_desc = res_desc
    st.markdown('</div>', unsafe_allow_html=True)

    if 'final_desc' in st.session_state:
        st.markdown(f'<div class="desc-box">{st.session_state.final_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tags & Hashtags (Ảnh 846)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 25 TỪ KHÓA TỐI ƯU")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data['tags']])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.subheader("#️⃣ HASHTAGS")
    st.code(" ".join(data['hashtags']))
    st.subheader("💬 BÌNH LUẬN MẪU")
    st.info(data['pinned'])
    st.markdown('</div>', unsafe_allow_html=True)
