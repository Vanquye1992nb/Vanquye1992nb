import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN MẪU (Ảnh 843, 844) ---
st.set_page_config(page_title="Hệ Thống SEO AI Pro v5", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    h1, h2, h3, p, label { color: #f8fafc !important; font-weight: bold; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); 
        backdrop-filter: blur(10px);
        padding: 25px; 
        border-radius: 16px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        margin-bottom: 20px;
    }
    .main-title { 
        background: linear-gradient(90deg, #f1c40f, #e67e22);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 38px; font-weight: 900; text-align: center; margin-bottom: 15px; 
    }
    .stButton>button { 
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important; color: white !important; 
        width: 100%; border-radius: 10px; height: 3.5em; font-weight: 800; border: none;
    }
    .tag-bubble { 
        background: linear-gradient(135deg, #334155, #1e293b); color: #60a5fa; 
        padding: 8px 16px; border-radius: 20px; display: inline-block; margin: 5px; 
        border: 1px solid #475569; font-size: 13px;
    }
    .desc-box { background: #0f172a; padding: 15px; border-radius: 10px; border: 1px dashed #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG AI TỰ ĐỘNG CHỌN MODEL (CHỐNG LỖI 404) ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Chuyển priorities về Gemini 1.5/1.0
        priorities = ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro-latest', 'models/gemini-pro']
        for p in priorities:
            if p in models: return genai.GenerativeModel(p)
        return genai.GenerativeModel(models[0])
    except: return None

# --- 3. LOGIC XỬ LÝ DỮ LIỆU ---
def call_gemini_safe(model, prompt, max_retries=3):
    for i in range(max_retries):
        try:
            return model.generate_content(prompt).text
        except Exception as e:
            if "ResourceExhausted" in str(e) or "429" in str(e):
                st.warning(f"⚠️ Hạn mức API tạm thời hết. AI đang thử lại sau { (i+1)*5 } giây...")
                time.sleep((i+1)*5) # Thử lại sau 5, 10, 15 giây
            else: return None
    return "ERROR_QUOTA"

# --- 4. GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-title">HỆ THỐNG SEO AI TOÀN DIỆN</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ KẾT NỐI API")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    st.warning("Nếu bị lỗi 429, hãy đợi 60 giây.")

# KHỐI 1: NHẬP LIỆU
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"]); ref = st.text_input("Link đối thủ")
    with c2: kw = st.text_input("Từ khóa chính (Bắt buộc)"); channel = st.text_input("Kênh của bạn")
    
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH SEO"):
        if kw and api_key:
            with st.spinner("AI đang cào dữ liệu..."):
                model = get_model(api_key)
                prompt = f"SEO Youtube cho '{kw}' ({lang}). Link: {ref}. Trả về JSON: 'titles'(10), 'tags'(25), 'hashtags'(10), 'pinned'."
                res = call_gemini_safe(model, prompt)
                
                if res == "ERROR_QUOTA": st.error("⚠️ Bạn đã hết hạn mức API miễn phí (Lỗi 429).")
                elif res:
                    try:
                        data = json.loads(re.search(r'\{.*\}', res, re.DOTALL).group())
                        st.session_state.seo_data = data
                        st.session_state.kw = kw
                    except: st.error("Lỗi định dạng AI. Hãy thử lại.")
        else: st.warning("⚠️ Vui lòng điền đủ Từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# KHỐI 2: KẾT QUẢ SEO (Trên cùng 1 trang)
if 'seo_data' in st.session_state:
    data = st.session_state.seo_data
    
    # 2.1 Tiêu đề & Chọn mô tả (Ảnh 845)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏅 10 TIÊU ĐỀ HẤP DẪN")
    for t in data.get('titles', []): st.write(f"🎯 {t}")
    st.divider()
    selected_title = st.selectbox("Chọn tiêu đề để viết mô tả chi tiết:", data.get('titles', []))
    if st.button("📝 VIẾT MÔ TẢ CHO TIÊU ĐỀ NÀY"):
        with st.spinner("Đang soạn mô tả..."):
            model = get_model(api_key)
            prompt_desc = f"Viết mô tả Youtube chuẩn SEO cho: '{selected_title}'. Có bao gồm kêu gọi đăng ký."
            st.session_state.desc_res = call_gemini_safe(model, prompt_desc, max_retries=1)
    if 'desc_res' in st.session_state:
        st.markdown(f'<div class="desc-box">{st.session_state.desc_res}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.2 Tags & Hashtags (Ảnh 846, 9e1976)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 25 THẺ TAGS SEO TỐI ƯU")
    tags_html = "".join([f'<span class="tag-bubble">{t}</span>' for t in data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.divider()
    c_h, c_p = st.columns(2)
    with c_h: st.subheader("#️⃣ HASHTAGS"); st.code(" ".join(data.get('hashtags', [])))
    with c_p: st.subheader("💬 BÌNH LUẬN GHIM"); st.info(data.get('pinned', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # 2.3 Công cụ tạo Prompt ảnh - Tích hợp Nano Banana 2 (Ảnh 847)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 CÔNG CỤ TẠO THUMBNAIL (NANO BANANA 2)")
    style = st.radio("Chọn phong cách", [" Realistic", " Comic Book", " 3D Disney"], horizontal=True)
    
    # Ép dùng Nano Banana 2
    if st.button("✨ TẠO PROMPT ẢNH MINH HỌA (BANANA v2)"):
        with st.spinner("Đang kết nối model Nano Banana 2..."):
            model_banana = genai.GenerativeModel('gemini-nano-banana-2')
            
            prompt_banana = f"""
            Bạn là model 'Nano Banana 2' chuyên tạo prompt ảnh nghệ thuật.
            Dựa trên video Youtube có tiêu đề: '{selected_title}' và phong cách {style}.
            Hãy tạo một prompt tiếng Anh siêu chi tiết để vẽ ảnh, cinematic lighting, ultra-high resolution, vivid colors.
            Mô tả chính xác chủ thể, hành động, bối cảnh, cảm xúc.
            """
            banana_res = call_gemini_safe(model_banana, prompt_banana)
            st.session_state.banana_prompt = banana_res
            
    if 'banana_prompt' in st.session_state:
        st.caption("Copy prompt dưới đây dán vào model Nano Banana Pro để vẽ:")
        st.code(st.session_state.banana_prompt, language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)
