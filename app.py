import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); padding: 25px; 
        border-radius: 15px; border: 1px solid #475569; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .tag-chip { background: #334155; color: #60a5fa; padding: 5px 12px; border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #475569; }
    /* Màu nút bấm theo ảnh 844 */
    .btn-blue button { background: #2563eb !important; color: white !important; }
    .btn-green button { background: #10b981 !important; color: white !important; }
    .btn-purple button { background: #9333ea !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG GỌI AI ĐA TẦNG (FIX LỖI 404 & 429) ---
def call_ai_ultimate(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        
        # Danh sách model dự phòng để tránh lỗi 404
        # Thử nghiệm với các tên gọi model phổ biến nhất
        model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-pro-latest', 'gemini-pro']
        
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Cơ chế chờ đợi nếu gặp lỗi 429
                for i in range(2):
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            return response.text
                    except Exception as e:
                        if "429" in str(e):
                            time.sleep(5) # Nghỉ 5 giây nếu hết hạn mức
                            continue
                        raise e
            except Exception as e:
                if "404" in str(e): # Nếu không thấy model này, thử model tiếp theo
                    continue
                return f"LỖI: {str(e)}"
        
        return "LỖI: Không thể kết nối với bất kỳ Model Gemini nào. Hãy kiểm tra lại API Key."
    except Exception as e:
        return f"LỖI HỆ THỐNG: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH (THEO ẢNH 843) ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ CÀI ĐẶT")
    key = st.text_input("Gemini API Key", type="password")
    st.info("Sử dụng model Gemini 1.5 Flash ổn định.")

# KHỐI NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref_link = st.text_input("Link video đối thủ (Tùy chọn)")
    with c2:
        keyword = st.text_input("Từ khóa chính (Bắt buộc)")
        my_channel = st.text_input("Tên kênh của bạn")
    
    if st.button("🚀 TẠO NỘI DUNG TỐI ƯU", use_container_width=True):
        if not key or not keyword:
            st.error("Thiếu API Key hoặc Từ khóa!")
        else:
            with st.spinner("Đang phân tích dữ liệu..."):
                main_prompt = f"""Bạn là một chuyên gia SEO YouTube. Hãy phân tích từ khóa '{keyword}' ({lang}). 
                Yêu cầu trả về dữ liệu dưới dạng JSON (không có markdown):
                {{
                    "titles": ["10 tiêu đề thu hút"],
                    "tags": ["25 tags SEO"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "Bình luận ghim mẫu"
                }}"""
                res = call_ai_ultimate(key, main_prompt)
                
                if "LỖI" in res:
                    st.error(res)
                else:
                    try:
                        # Làm sạch chuỗi để lấy đúng JSON
                        json_str = re.search(r'\{.*\}', res, re.DOTALL).group()
                        st.session_state.seo_res = json.loads(json_str)
                        st.session_state.saved_kw = keyword
                    except:
                        st.error("Dữ liệu AI trả về bị lỗi định dạng. Thử lại sau 10 giây.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI HIỂN THỊ KẾT QUẢ
if 'seo_res' in st.session_state:
    data = st.session_state.seo_res
    
    # Nhóm nút công cụ theo ảnh 844
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with col_b2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with col_b3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # Tiêu đề
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🏅 10 TIÊU ĐỀ SEO CHO: {st.session_state.saved_kw.upper()}")
    for i, t in enumerate(data.get('titles', []), 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    selected_title = st.selectbox("Chọn tiêu đề để tạo mô tả:", data.get('titles', []))
    if st.button("📝 TẠO MÔ TẢ CHI TIẾT"):
        with st.spinner("AI đang soạn mô tả..."):
            desc_p = f"Viết mô tả YouTube chuẩn SEO cho video tiêu đề: '{selected_title}'"
            st.session_state.final_desc = call_ai_ultimate(key, desc_p)
    
    if 'final_desc' in st.session_state:
        st.info(st.session_state.final_desc)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tag & Hashtag
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    cl, cr = st.columns([2, 1])
    with cl:
        st.subheader("📊 25 TỪ KHÓA SEO")
        tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in data.get('tags', [])])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.text_area("Copy tags:", ", ".join(data.get('tags', [])), height=70)
    with cr:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
        st.subheader("📌 BÌNH LUẬN GHIM")
        st.caption(data.get('pinned', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # Thumbnail
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 Ý TƯỞNG THUMBNAIL")
    if st.button("✨ TẠO PROMPT ẢNH"):
        prompt_image = f"Tạo prompt vẽ ảnh thumbnail cho video: {selected_title}"
        st.code(call_ai_ultimate(key, prompt_image))
    st.markdown('</div>', unsafe_allow_html=True)
