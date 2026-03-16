import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN (Fix lỗi mất tiêu đề) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiển thị tiêu đề các ô nhập liệu trắng rõ */
    label, .stMarkdown p { 
        color: #ffffff !important; 
        font-weight: 600 !important;
        display: block !important;
        margin-bottom: 5px !important;
    }

    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px;
    }

    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }

    /* Nút Tạo Nội Dung (Xanh dương) */
    .stButton>button { 
        background: #2563eb !important; color: white !important; 
        border-radius: 8px; height: 3.5em; font-weight: bold; border: none;
    }

    /* Thẻ tag (Ảnh 846) */
    .tag-chip { 
        background: #4a5568; color: #e2e8f0; padding: 6px 14px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM AI: FIX 404 & FIX KHÔNG RA TIN ---
def process_seo(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model định danh đầy đủ để tránh 404
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        prompt = f"""
        Nhiệm vụ: SEO Youtube cho từ khóa '{keyword}'.
        Hãy trả về 1 chuỗi JSON duy nhất, không có văn bản thừa:
        {{
            "trend": "mô tả xu hướng hiện tại",
            "titles": ["tiêu đề 1", "tiêu đề 2", ..., "tiêu đề 10"],
            "tags": ["tag 1", "tag 2", ..., "tag 25"],
            "desc": "mô tả video chuẩn SEO",
            "comment": "bình luận ghim hay"
        }}
        """
        response = model.generate_content(prompt)
        
        # Dùng Regex để lấy đúng phần JSON (Fix lỗi không ra tin)
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
        return None

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Gemini API Key:", type="password")
    if st.button("🔄 Làm mới ứng dụng"):
        st.session_state.clear()
        st.rerun()

# --- BƯỚC 1: FORM NHẬP LIỆU (Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: cách nấu phở", key="kw_input")
            st.text_input("Link kênh của bạn", placeholder="Dán link kênh...", key="chan")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang tra cứu dữ liệu..."):
                    result = process_seo(api_key, kw)
                    if result:
                        st.session_state.data = result
                        st.session_state.kw = kw
                        st.session_state.step = 2
                        st.rerun()
            else: st.warning("Vui lòng nhập đầy đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (Ảnh 844, 845, 846) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📈 KẾT QUẢ SEO: {st.session_state.kw.upper()}")
    
    # 3 Nút chức năng (Ảnh 844)
    st.write("🚀 CÔNG CỤ PHÂN TÍCH:")
    bc1, bc2, bc3 = st.columns(3)
    bc1.button("🔵 Danh mục", type="primary")
    bc2.button("🟢 Thẻ Tag", type="secondary")
    bc3.button("🟣 Thông tin", type="secondary")

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.info(t)
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.divider()
    if st.button("🔄 Tạo từ khóa khác"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
