import streamlit as st
import google.generativeai as genai
import json
import re
import time

# --- 1. CẤU HÌNH GIAO DIỆN (THEO MẪU GỐC) ---
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

# --- 2. HÀM XỬ LÝ AI "BẤT BẠI" (CHỐNG 404 & 429) ---
def call_gemini_smart(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        
        # Thử lần lượt các model để tránh lỗi 404 (Model Not Found)
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Cơ chế Retry khi gặp lỗi 429 (Resource Exhausted)
                for attempt in range(2):
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            return response.text
                    except Exception as e:
                        if "429" in str(e):
                            time.sleep(3) # Đợi 3 giây rồi thử lại
                            continue
                        raise e
            except Exception as e:
                last_error = str(e)
                continue # Thử model tiếp theo
        
        if "429" in last_error: return "LIMIT_REACHED"
        return f"LỖI: {last_error}"
    except Exception as e:
        return f"HỆ THỐNG LỖI: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown('<p class="title-gold">🚀 TRỢ LÝ SEO VIDEO AI VĂN THẾ</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 CÀI ĐẶT API")
    api_key = st.text_input("Nhập Gemini API Key", type="password")
    st.info("Bản cập nhật đã sửa lỗi model 404 và trích xuất JSON.")

# KHỐI NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("Link đối thủ (Tùy chọn)")
    with c2:
        kw = st.text_input("Từ khóa chính (Bắt buộc)")
        channel = st.text_input("Tên/Link kênh")
    
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH SEO", type="primary"):
        if not api_key or not kw:
            st.warning("Vui lòng nhập API Key và Từ khóa.")
        else:
            with st.spinner("AI đang làm việc..."):
                prompt = f"""SEO Youtube '{kw}' ({lang}). Cần JSON chuẩn (không Markdown):
                {{
                    "titles": ["10 tiêu đề"],
                    "tags": ["25 tags"],
                    "hashtags": ["10 hashtags"],
                    "pinned": "ghim",
                    "comment_rival": "mẫu"
                }}"""
                res = call_gemini_smart(api_key, prompt)
                
                if res == "LIMIT_REACHED":
                    st.error("⚠️ Hết hạn mức API miễn phí. Vui lòng đợi 60 giây.")
                elif res.startswith("LỖI"):
                    st.error(res)
                else:
                    try:
                        # Dọn dẹp văn bản để lấy đúng JSON
                        clean_json = re.search(r'\{.*\}', res, re.DOTALL).group()
                        st.session_state.seo_data = json.loads(clean_json)
                        st.session_state.current_kw = kw
                    except:
                        st.error("AI phản hồi sai định dạng dữ liệu. Hãy thử lại.")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI KẾT QUẢ
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # 3 Nút chức năng mẫu ảnh 844
    cb1, cb2, cb3 = st.columns(3)
    with cb1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("🔍 Kiểm tra danh mục"); st.markdown('</div>', unsafe_allow_html=True)
    with cb2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("🏷️ Thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with cb3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị Tiêu đề & Mô tả
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🏅 KẾT QUẢ CHO: {st.session_state.current_kw.upper()}")
    titles = data.get('titles', [])
    for i, t in enumerate(titles, 1):
        st.write(f"**{i}.** {t}")
    
    st.divider()
    sel_title = st.selectbox("Chọn tiêu đề để viết mô tả:", titles)
    if st.button("📝 VIẾT MÔ TẢ SEO CHI TIẾT"):
        with st.spinner("Đang soạn..."):
            d_prompt = f"Viết mô tả Youtube chuẩn SEO cho: {sel_title}"
            desc_res = call_gemini_smart(api_key, d_prompt)
            st.session_state.final_desc = desc_res
            
    if 'final_desc' in st.session_state:
        st.markdown(f'<div class="desc-output">{st.session_state.final_desc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tags & Hashtags
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_tags, col_extra = st.columns([2, 1])
    with col_tags:
        st.subheader("📊 25 TỪ KHÓA SEO")
        tags = data.get('tags', [])
        st.markdown("".join([f'<span class="tag-chip">{tag}</span>' for tag in tags]), unsafe_allow_html=True)
        st.text_area("Copy bộ Tag:", ", ".join(tags), height=100)
    with col_extra:
        st.subheader("#️⃣ HASHTAGS")
        st.code(" ".join(data.get('hashtags', [])))
        st.subheader("💬 BÌNH LUẬN GHIM")
        st.info(data.get('pinned', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # Thumbnail Tool (Nano Banana 2 Prompt)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 Ý TƯỞNG THUMBNAIL (NANO BANANA 2)")
    t_text = st.text_input("Văn bản chính trên ảnh", value="VĂN THẾ SEO")
    if st.button("🖼️ TẠO PROMPT ẢNH"):
        p_thumb = f"Tạo prompt vẽ ảnh thumbnail Youtube cho tiêu đề '{sel_title}' có chữ '{t_text}'"
        st.code(call_gemini_smart(api_key, p_thumb))
    st.markdown('</div>', unsafe_allow_html=True)
