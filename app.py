import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 初始化 Session State 用於管理搜尋紀錄
if 'search_val' not in st.session_state:
    st.session_state.search_val = ""

# 定義切換分類時清空搜尋的函數
def clear_search():
    st.session_state.search_val = ""

# 2. 終極 CSS 樣式：修復商品說明顏色、Top Bar 右側與移除 Tab 背景色
st.markdown("""
    <style>
    /* 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6 !important;
    }

    /* --- 1. 最上方 Top Bar (Header) 徹底黑化 --- */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
        border-bottom: 1px solid #e0e0e0;
    }
    /* 強制 Header 內所有按鈕、圖示（包含右側 GitHub/Share）變黑 */
    header[data-testid="stHeader"] * {
        color: #000000 !important;
        fill: #000000 !important;
    }

    /* --- 2. 側邊欄：白色背景 + 純黑文字 --- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stSidebar"] .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #d0d0d0 !important;
    }

    /* --- 3. 商品頁面文字黑化 (關鍵修復) --- */
    /* 強制 Explore 標題、產品名稱變黑 */
    h1, h2, h3, [data-testid="stHeader"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* 【修復重點】強制商品卡片內的說明文字變黑 */
    .product-box p, .product-box span, .product-box div, .main p {
        color: #000000 !important;
        font-weight: 400 !important;
        opacity: 1 !important;
    }

    /* --- 4. 產品卡片與柔和沙褐色按鈕 --- */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px; margin-bottom: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #eef0f2;
    }
    .stLinkButton > a {
        background-color: #A68966 !important; 
        color: #ffffff !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 10px 30px !important;
    }

    /* --- 5. 分類 Tabs 優化：深咖啡色，移除底色色塊 --- */
    .stTabs [data-baseweb="tab"] {
        color: #444444 !important;
        font-weight: bold !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #5D4037 !important; /* 深咖啡色文字 */
        border-bottom: 3px solid #3E2723 !important; /* 深咖啡色底線 */
        background-color: transparent !important;
    }

    /* 圖片顯示限制 */
    .stImage img { max-height: 180px; width: auto; object-fit: contain; border-radius: 8px; }
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
    st.error(f"Excel 讀取失敗: {e}"); st.stop()

# 4. 側邊欄導航 (整合清空搜尋功能)
with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Top Choice", "CC Picks"],
        index=0,
        on_change=clear_search
    )
    search_query = st.text_input(
        "🔍 Search ALL Products", 
        placeholder="Search anything...",
        key="search_val"
    )

# 5. 商品渲染函數
def render_item_list(data):
    for _, row in data.iterrows():
        # 套用 .product-box 樣式
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) 
        with col1:
            img_path = f"image/{row['Image_URL']}"
            st.image(img_path, use_container_width=True)
        with col2:
            st.subheader(row['Product_Name'])
            if st.session_state.search_val:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            # 這裡的文字現在會被強制設為黑色
            st.write(row['Description'])
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 主要顯示邏輯
if st.session_state.search_val:
    st.title(f"🔍 Results: '{st.session_state.search_val}'")
    results = df[df['Product_Name'].str.contains(st.session_state.search_val, case=False, na=False) | 
              df['Description'].str.contains(st.session_state.search_val, case=False, na=False)]
    if results.empty:
        st.info("No matching products found.")
    else:
        render_item_list(results)
else:
    st.title(f"Explore: {main_page}")
    source_map = {"Toronto Base": "Toronto Base", "Amazon Top Choice": "Amazon Top Choice", "CC Picks": "CC Picks"}
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    if page_df.empty:
        page_df = df[df[target_col] == main_page.split()[0]]

    if not page_df.empty:
        unique_cats = page_df['Category'].unique().tolist()
        tabs = st.tabs(unique_cats)
        for i, cat in enumerate(unique_cats):
            with tabs[i]:
                render_item_list(page_df[page_df['Category'] == cat])
    else:
        st.warning(f"No items found for {main_page}.")

st.divider()
st.caption("© 2026 CC Picks the World | As an Amazon Associate, I earn from qualifying purchases.")
