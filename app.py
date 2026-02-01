import streamlit as st

# 1. 網頁基礎設定：將佈局設為寬廣模式
st.set_page_config(page_title="Toronto Living | Curated Picks", page_icon="🍁", layout="wide")

# 2. 進階 CSS：強化卡片與按鈕視覺
st.markdown("""
    <style>
    /* 整體背景與字體 */
    .main { background-color: #ffffff; color: #333333; }
    
    /* 產品卡片效果 */
    .product-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    /* Amazon 橘色按鈕優化 */
    .stLinkButton>a {
        background-color: #FF9900 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 標題區塊
st.title("🍁 Toronto Life: The Ultimate Amazon Guide")
st.write("Expert-picked essentials for stylish and functional GTA apartment living.")
st.divider()

# 4. 產品區塊 (卡片式佈局)
def product_row(img_url, title, features, link):
    with st.container():
        col1, col2 = st.columns([1, 1.5], gap="large")
        with col1:
            st.image("candle.jpg", use_container_width=True)
        with col2:
            st.header(title)
            for f in features:
                st.write(f"- {f}")
            st.link_button(f"Check Price on Amazon.ca", link)
        st.divider()

# 產品列表：請確保圖片連結有效
product_row(
    "https://m.media-amazon.com/images/I/71wLp9M6XSL._AC_SL1500_.jpg", 
    "Aesthetic Candle Warmer Lamp",
    ["Fire-Safe: Perfect for Toronto Condos", "Cozy Glow for long GTA winters", "Extended candle life"],
    "https://amzn.to/4k9N2O1"
)

product_row(
    "https://m.media-amazon.com/images/I/716m2zS6+pL._AC_SL1500_.jpg",
    "Ergonomic Laptop Stand",
    ["Essential for WFH / International Students", "Saves desk space in compact dens", "Improves study posture"],
    "https://amzn.to/your_link" # 記得換成你的連結
)

# 5. 法律聲明
st.caption("As an Amazon Associate, I earn from qualifying purchases. #ad")