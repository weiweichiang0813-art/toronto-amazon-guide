import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. CSS 樣式：限制圖片高度與縮小顯示
st.markdown("""
    <style>
    /* 1. 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6;
    }

    /* 2. 標題與一般文字：改為深灰色/深藍色，確保清晰 */
    h1, h2, h3 {
        color: #232f3e !important; /* 深亞馬遜藍 */
        font-weight: 800 !important;
    }
    
    p, span, label {
        color: #444444 !important; /* 標準深灰，不刺眼但清晰 */
    }

    /* 3. 產品卡片：純白背景 + 陰影，讓它從灰色背景跳脫出來 */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* 加深陰影，增加立體感 */
        border: 1px solid #e0e0e0;
    }

    /* 4. 側邊欄：稍微調暗，區分功能區 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
    }

    /* 5. 圖片控制：限制高度 */
    .stImage img {
        max-height: 180px;
        width: auto;
        object-fit: contain;
        border-radius: 8px;
    }

    /* 6. Tabs 選項卡：加強選中時的顏色 */
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
        color: #666;
    }
    .stTabs [aria-selected="true"] {
        color: #FF9900 !important; /* 選中時顯示亞馬遜橘 */
        border-bottom-color: #FF9900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取數據
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    target_col = "Source" if "Source" in df.columns else "Sources"
    
    # 清理資料內容
    for col in [target_col, 'Category', 'Product_Name', 'Image_URL']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
except Exception as e:
    st.error(f"Excel 讀取失敗: {e}")
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
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        # 使用 [1, 4] 比例讓圖片佔位更小
        col1, col2 = st.columns([1, 4]) 
        with col1:
            # 根據你的 GitHub 資料夾名稱，補上 "image/" 路徑
            img_path = f"image/{row['Image_URL']}"
            if os.path.exists(img_path) or row['Image_URL'].startswith('http'):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("圖片遺失")
        with col2:
            st.subheader(row['Product_Name'])
            if search_query:
                st.caption(f"Location: {row[target_col]} | Category: {row['Category']}")
            st.write(row['Description'])
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()

# 6. 主要顯示邏輯
if search_query:
    st.title(f"🔍 Search Results: '{search_query}'")
    results = df[
        df['Product_Name'].str.contains(search_query, case=False, na=False) |
        df['Description'].str.contains(search_query, case=False, na=False)
    ]
    if results.empty:
        st.info("No matching products found.")
    else:
        render_item_list(results)
else:
    st.title(f"Explore: {main_page}")
    
    # 對應 Excel 內的標籤內容 (請根據你的 Excel 實際填寫內容微調)
    source_map = {
        "Toronto Base": "Toronto Base",
        "Amazon Top Choice": "Amazon Top Choice",
        "CC Picks": "CC Picks"
    }
    
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    if page_df.empty:
        # 如果找不到，嘗試抓簡稱 (Toronto/Amazon/CC)
        short_tag = main_page.split()[0]
        page_df = df[df[target_col] == short_tag]

    if page_df.empty:
        st.warning(f"目前在 '{current_tag}' 找不到商品。")
        st.write("Excel 內現有的標籤：", df[target_col].unique().tolist())
    else:
        unique_cats = page_df['Category'].unique().tolist()
        tabs = st.tabs(unique_cats)
        for i, cat in enumerate(unique_cats):
            with tabs[i]:
                render_item_list(page_df[page_df['Category'] == cat])

st.caption("© 2026 CC Picks the World | As an Amazon Associate, I earn from qualifying purchases.")


