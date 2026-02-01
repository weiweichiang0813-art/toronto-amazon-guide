import streamlit as st
import pandas as pd

# 1. 網頁基礎配置
st.set_page_config(page_title="CC Picks the World", page_icon="🔍", layout="wide")

# 2. 專業 CSS 樣式 (優化陰影與導航)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .product-box {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #efefef;
    }
    .stLinkButton>a {
        background-color: #FF9900 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
    }
    /* 頂部 Banner 樣式 */
    .top-banner {
        background-color: #232f3e;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部 Banner 與 基本功能 ---
st.markdown('<div class="top-banner"><h1>🌎 CC Picks the World</h1></div>', unsafe_allow_html=True)

# 模擬一般網站的功能按鈕 (Home, Search, About)
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
with col_nav1:
    if st.button("🏠 Home"): st.rerun()
with col_nav2:
    st.button("ℹ️ About")

# 搜尋框置頂
search_query = st.text_input("🔍 Search for products, brands, or styles...", placeholder="Try 'Winter Coat' or 'Earrings'")

# --- 側邊欄導覽 ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Collection", ["📍 Toronto Base", "🔥 Amazon Top Choice", "✨ CC Picks"])

# 3. 讀取數據與渲染函數
def display_products(df, category_filter):
    # 根據分類過濾數據
    if category_filter != "All":
        filtered_df = df[df['Category'] == category_filter]
    else:
        filtered_df = df
        
    # 如果有搜尋關鍵字
    if search_query:
        filtered_df = filtered_df[filtered_df['Product_Name'].str.contains(search_query, case=False) | 
                                  filtered_df['Description'].str.contains(search_query, case=False)]

    if filtered_df.empty:
        st.warning("No products found in this category.")
        return

    for index, row in filtered_df.iterrows():
        with st.container():
            # 使用自定義 CSS 類名包裝
            st.markdown('<div class="product-box">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2], gap="large")
            with col1:
                st.image(row['Image_URL'], use_container_width=True)
            with col2:
                st.subheader(row['Product_Name'])
                st.caption(f"Category: {row['Category']}")
                st.write(row['Description'])
                st.link_button(f"Buy for ${row['Price']} on Amazon", row['Affiliate_Link'])
            st.markdown('</div>', unsafe_allow_html=True)

# --- 主程式邏輯 ---
try:
    # 讀取 Excel (建議多加一個 'Source' 欄位來區分 Toronto/Amazon/CC)
    df = pd.read_excel("my_products.xlsx")
    
    # 建立頁面內容
    st.title(f"{page}")
    
    # 在頁面內建立分類 Tabs
    tab1, tab2, tab3 = st.tabs(["👗 Clothing", "💎 Accessories", "📦 Others"])
    
    # 根據頁面決定顯示哪些數據 (這裡假設你的 Excel 有一個 'Source' 欄位)
    # 如果還沒有 Source 欄位，這部分可以先註解掉或根據類別篩選
    source_map = {
        "📍 Toronto Base": "Toronto",
        "🔥 Amazon Top Choice": "Amazon",
        "✨ CC Picks": "CC"
    }
    
    current_source = source_map[page]
    page_df = df[df['Source'] == current_source] if 'Source' in df.columns else df

    with tab1:
        display_products(page_df, "Clothing")
    with tab2:
        display_products(page_df, "Accessories")
    with tab3:
        display_products(page_df, "Others")

except Exception as e:
    st.error(f"Error: {e}")
    st.info("請確保 'my_products.xlsx' 包含以下欄位: Product_Name, Category, Description, Image_URL, Affiliate_Link, Price, Source")

st.divider()
st.caption("As an Amazon Associate, I earn from qualifying purchases.")
