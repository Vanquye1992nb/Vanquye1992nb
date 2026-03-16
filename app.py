import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CẤU HÌNH GIAO DIỆN DARK MODE ---
st.set_page_config(page_title="Tool Tìm Key Youtube Văn Thế Web", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); 
        color: black; font-weight: bold; border: none; border-radius: 10px; height: 3.5em;
    }
    .header-text { color: #f1c40f; text-align: center; font-weight: bold; font-size: 35px; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #888; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="header-text">🖥️ Tool Tìm Key Youtube Văn Thế Web AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Công cụ tự động hóa nghiên cứu từ khóa nâng cấp bởi Gemini AI</p>', unsafe_allow_html=True)

# --- SIDEBAR: CẤU HÌNH API ---
with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", help="Lấy key tại aistudio.google.com")
    st.markdown("---")
    st.write("📌 **Hướng dẫn:**")
    st.write("1. Dán API Key vào ô trên")
    st.write("2. Nhập chủ đề video")
    st.write("3. Nhấn 'Tìm kiếm' và đợi AI trả kết quả")

# --- LAYOUT CHÍNH ---
col1, col2 = st.columns(2)

with col1:
    chu_de = st.text_input("# Chủ Đề (Bắt buộc)", placeholder="vd: Hoạt hình, Mukbang AI, Sinh tồn")
    st.button("💡 Danh sách gợi ý chủ đề")
    tu_khoa_phu = st.text_input("# Từ Khóa Chính (Tùy chọn)", placeholder="vd: tu tiên, rèn luyện")

with col2:
    ngon_ngu = st.selectbox("🌐 Ngôn Ngữ", ["Tiếng Việt", "English", "Japanese"])
    doi_tuong = st.selectbox("👥 Đối Tượng Mục Tiêu", ["View Việt", "View Quốc Tế"])
    so_luong = st.slider("🔍 Số lượng từ khóa muốn tìm", 5, 30, 10)

# --- XỬ LÝ DỮ LIỆU ---
if st.button("🚀 TÌM KIẾM TỪ KHÓA NÂNG CAO"):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở cột bên trái!")
    elif not chu_de:
        st.warning("⚠️ Bạn chưa nhập chủ đề video!")
    else:
        try:
            # Khởi tạo AI
            genai.configure(api_key=api_key)
            # Sử dụng gemini-1.5-flash với cấu hình chuẩn
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('🎯 AI đang phân tích thị trường YouTube...'):
                prompt = f"""
                Bạn là một chuyên gia SEO YouTube chuyên nghiệp. 
                Hãy phân tích chủ đề '{chu_de}' với từ khóa phụ '{tu_khoa_phu}'.
                Tìm {so_luong} từ khóa tiềm năng cho {doi_tuong} bằng {ngon_ngu}.
                Yêu cầu: Trả về kết quả dưới dạng BẢNG gồm các cột: 
                STT, Từ khóa, Độ khó (%), Lượng tìm kiếm, Xu hướng.
                Cuối cùng hãy đưa ra 1 lời khuyên chiến lược để video này lên xu hướng.
                """
                
                response = model.generate_content(prompt)
                
                # Hiển thị kết quả
                st.success("✅ Đã phân tích xong!")
                st.markdown("### 📊 Bảng phân tích từ khóa ngách:")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
            st.info("Mẹo: Nếu gặp lỗi 404, hãy kiểm tra lại API Key hoặc thử lại sau ít phút.")

st.markdown("---")
st.caption("© 2026 Developed for Van The Web Team - Powered by Gemini Pro v1.5")
