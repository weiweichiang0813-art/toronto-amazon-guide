import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 初始化 Session State (如果不存在)
if 'search_val' not in st.session_state:
    st.session_state.search_val = ""

# 定義清空搜尋的函數
def clear_search():
    st.session_state.search_val = ""

# 2. 終極 CSS 樣式
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6 !important; }
    header[data-testid="stHeader"] { background-color: #ffffff !important; }
    
    /* 側邊欄與文字黑化 */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #000000 !important; font-weight: 600 !important;
    }

    /* 搜尋框優化：白底黑字 */
    div[data-testid="stSidebar"] .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #d0d0d0 !important;
        border-radius: 8px !important;
    }

    /* 主內容區標題與文字強制黑化 */
    h1, h2, h3, .main p, .main span, .main div {
        color: #000000 !important;
    }

    .product-box {
        background-color: #ffffff !important;
        padding: 25px; margin-bottom: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
    }

    .stLinkButton > a {
        background-color: #FF9900 !important; color: #ffffff !important;
        border-radius: 20px !important; padding: 12px 35px !important;
        font-weight: bold !important; text-decoration: none !important;
    }
    
    .stImage img { max-height: 200px; width: auto; object-fit: contain; }
    .stTabs [data-baseweb="tab"] { color: #000000 !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { color: #FF9900 !important; border-bottom-color: #FF9900 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取數據
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    target_col = "Source" if "Source" in df.columns else "Sources"
    for col in [target_col, 'Category', 'Product_Name', 'Image_URL']:
        if col in df.columns: df[col] = df[col].astype(str).str.strip()
except Exception as e:
    st.error(f"Excel 讀取失敗: {e}"); st.stop()

# 4. 側邊欄導航
with st.sidebar:
    st.title("📍 Navigation")
    # 當點選分類時，觸發 clear_search 函數
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Top Choice", "CC Picks"],
        index=0,
        on_change=clear_search
    )
    # 綁定 key 到 session_state
    search_query = st.text_input(
        "🔍 Search ALL Products", 
        placeholder="Search anything...",
        key="search_val"
    )

# 5. 商品渲染函數
def render_item_list(data):
    for _, row in data.iterrows():
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) 
        with col1:
            st.image(f"image/{row['Image_URL']}", use_container_width=True)
        with col2:
            st.subheader(row['Product_Name'])
            if st.session_state.search_val:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            st.write(row['Description'])
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 主要顯示邏輯
# 使用 st.session_state.search_val 代替搜尋判斷
if st.session_state.search_val:
    st.title(f"🔍 Results: '{st.session_state.search_val}'")
    results = df[df['Product_Name'].str.contains(st.session_state.search_val, case=False, na=False) | 
              df['Description'].str.contains(st.session_state.search_val, case=False, na=False)]
    if results.empty:
        st.info("No products found.")
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
