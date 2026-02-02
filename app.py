import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 專業 CSS 樣式：移除 Banner、美化側邊欄與產品卡片
st.markdown("""
    <style>
    /* 1. 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6;
    }

    /* 2. 側邊欄專屬樣式：白色背景 + 黑色文字 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 強制側邊欄內所有文字（標題、標籤、按鈕文字）為黑色 */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }

    /* 3. 搜尋欄位美化：確保在白色側邊欄內清晰 */
    .stTextInput input {
        background-color: #f9f9f9 !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }

    /* 4. 產品卡片美化：純白背景 + 陰影 */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }

    /* 5. 亞馬遜橘色按鈕 */
    .stLinkButton > a {
        background-color: #FF9900 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stLinkButton > a:hover {
        background-color: #e68a00 !important;
        color: #ffffff !important;
    }

    /* 6. 主內容區文字顏色：深色確保易讀 */
    .main h1, .main h2, .main h3, .main p, .main span {
        color: #232f3e !important;
    }

    /* 7. 圖片大小限制 */
    .stImage img {
        max-height: 180px;
        width: auto;
        object-fit: contain;
        border-radius: 8px;
    }

    /* 8. Tabs 分類選單顏色 */
    .stTabs [data-baseweb="tab"] {
        color: #666666 !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #FF9900 !important;
        border-bottom-color: #FF9900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取與清理數據
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

# 4. 側邊欄導航 (白色背景 + 黑色文字)
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
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) 
        with col1:
            # 自動指向 image 資料夾
            img_path = f"image/{row['Image_URL']}"
            st.image(img_path, use_container_width=True)
        with col2:
            st.subheader(row['Product_Name'])
            if search_query:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            st.write(row['Description'])
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 主要顯示邏輯 (已移除頂部 Banner)
if search_query:
    st.title(f"🔍 Results for: '{search_query}'")
    results = df[df['Product_Name'].str.contains(search_query, case=False, na=False) | 
              df['Description'].str.contains(search_query, case=False, na=False)]
    if results.empty:
        st.info("No matching products found.")
    else:
        render_item_list(results)
else:
    # 這裡直接顯示頁面標題，不再有 Banner
    st.title(f"Explore: {main_page}")
    
    source_map = {
        "Toronto Base": "Toronto Base", 
        "Amazon Top Choice": "Amazon Top Choice", 
        "CC Picks": "CC Picks"
    }
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    # 簡寫相容處理 (如 Toronto)
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
        st.warning(f"No items found for {main_page}. Check your Excel 'Source' column.")

st.divider()
st.caption("© 2026 CC Picks the World | As an Amazon Associate, I earn from qualifying purchases.")
