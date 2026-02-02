import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 專業 CSS 樣式：強制黑化文字，保留橘色按鈕
st.markdown("""
    <style>
    /* 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6;
    }

    /* --- 側邊欄：純白背景 + 純黑文字 --- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* --- 主內容區文字：強制改為純黑色 --- */
    /* 這裡處理標題、副標題與描述 */
    .main h1, .main h2, .main h3, .main .stHeader, .main subheader {
        color: #000000 !important;
    }
    
    /* 針對產品卡片內的文字特別強化 */
    .product-box h3 {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .product-box p, .product-box div, .main .stMarkdown p {
        color: #000000 !important;
        font-weight: 400 !important;
        line-height: 1.6;
    }

    /* --- 產品卡片美化 --- */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* 稍微加深陰影讓卡片更立體 */
        border: 1px solid #e0e0e0;
    }

    /* --- 按鈕：保留原本亮眼的橘色 --- */
    .stLinkButton > a {
        background-color: #FF9900 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 12px 35px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .stLinkButton > a:hover {
        background-color: #e68a00 !important;
        transform: scale(1.02); /* 增加一個微小的放大效果 */
    }

    /* 圖片顯示控制 */
    .stImage img {
        max-height: 200px;
        width: auto;
        object-fit: contain;
        border-radius: 10px;
    }

    /* Tabs 選項卡文字顏色 */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #FF9900 !important;
        border-bottom-color: #FF9900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取數據
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    target_col = "Source" if "Source" in df.columns else "Sources"
    
    for col in [target_col, 'Category', 'Product_Name', 'Image_URL']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
except Exception as e:
    st.error(f"讀取失敗: {e}")
    st.stop()

# 4. 側邊欄導航
with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Top Choice", "CC Picks"],
        index=0
    )
    search_query = st.text_input("🔍 Search ALL Products", placeholder="Search anything...")

# 5. 商品渲染函數
def render_item_list(data):
    for _, row in data.iterrows():
        # 套用自定義的產品卡片樣式
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) 
        with col1:
            img_path = f"image/{row['Image_URL']}"
            st.image(img_path, use_container_width=True)
        with col2:
            # 產品名稱：純黑
            st.subheader(row['Product_Name'])
            if search_query:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            # 產品描述：純黑
            st.write(row['Description'])
            # 按鈕：保持橘色
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 主要顯示邏輯
if search_query:
    st.title(f"🔍 Results: '{search_query}'")
    results = df[df['Product_Name'].str.contains(search_query, case=False, na=False) | 
              df['Description'].str.contains(search_query, case=False, na=False)]
    if results.empty:
        st.info("No matching products found.")
    else:
        render_item_list(results)
else:
    # 標題：純黑
    st.title(f"Explore: {main_page}")
    
    source_map = {
        "Toronto Base": "Toronto Base", 
        "Amazon Top Choice": "Amazon Top Choice", 
        "CC Picks": "CC Picks"
    }
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    if page_df.empty:
        short_tag = main_page.split()[0]
        page_df = df[df[target_col] == short_tag]

    if not page_df.empty:
        unique_cats = page_df['Category'].unique().tolist()
        tabs = st.tabs(unique_cats)
        for i, cat in enumerate(unique_cats):
            with tabs[i]:
                render_item_list(page_df[page_df['Category'] == cat])
    else:
        st.warning(f"No items found for {main_page}. Please check your Excel.")

st.divider()
st.caption("© 2026 CC Picks the World | As an Amazon Associate, I earn from qualifying purchases.")
