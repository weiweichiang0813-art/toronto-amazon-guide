import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. CSS 樣式：限制圖片高度與縮小顯示
st.markdown("""
    <style>
    /* 1. 修改全網頁背景為淺灰色 */
    .stApp {
        background-color: #f4f7f6; 
    }
    
    /* 2. 讓產品卡片變成白色，並加入陰影與圓角 */
    .product-box {
        background-color: #ffffff; /* 卡片背景為純白 */
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 15px; /* 圓角更明顯一點 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); /* 淡淡的陰影 */
        border: 1px solid #eeeeee;
    }

    /* 3. 圖片顯示控制 */
    .stImage img {
        max-height: 180px;
        width: auto;
        object-fit: contain;
        border-radius: 8px;
    }

    /* 4. 調整 Tab 標籤欄的背景（可選，讓它看起來更乾淨） */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
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

