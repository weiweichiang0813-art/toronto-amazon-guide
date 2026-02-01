import streamlit as st
import pandas as pd

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# --- 新增 CSS 樣式來限制圖片高度 ---
st.markdown("""
    <style>
    .stImage img {
        max-height: 200px; /* 你可以根據喜好調整這個數值，如 150px 或 250px */
        width: auto;
        object-fit: contain;
        border-radius: 10px; /* 順便加個小圓角更有質感 */
    }
    .product-container {
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 讀取數據
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    target_col = "Sources" if "Sources" in df.columns else "Source"
    
    df[target_col] = df[target_col].astype(str).str.strip()
    df['Category'] = df['Category'].astype(str).str.strip()
    df['Product_Name'] = df['Product_Name'].astype(str).str.strip()
except Exception as e:
    st.error(f"無法讀取 Excel: {e}")
    st.stop()

# 3. 側邊欄導航
with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Top Choice", "CC Picks"],
        index=0
    )
    search_query = st.text_input("🔍 Search ALL Products", placeholder="Search anything...")

# 4. 商品渲染函數 (已修改比例與圖片控制)
def render_item_list(data):
    for _, row in data.iterrows():
        # 使用 markdown 包裹一個 div 方便套用 CSS
        st.markdown('<div class="product-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) # 這裡調成 1:4，圖片欄位會變窄
        with col1:
            # 這裡我們保持 True，高度交給上面的 CSS 控制
            st.image(row['Image_URL'], use_container_width=True) 
        with col2:
            st.subheader(row['Product_Name'])
            if search_query:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            st.write(row['Description'])
            st
