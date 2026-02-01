import streamlit as st
import pandas as pd

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 讀取數據
try:
    df = pd.read_excel("my_products.xlsx")
    # 清理欄位空格，確保抓得到 Source 或 Sources
    df.columns = df.columns.str.strip()
    target_col = "Sources" if "Sources" in df.columns else "Source"
    
    # 清理儲存格內容空格
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
    # 全局搜尋框
    search_query = st.text_input("🔍 Search ALL Products", placeholder="Search anything...")

# 4. 商品渲染函數
def render_item_list(data):
    for _, row in data.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row['Image_URL'], use_container_width=True)
            with col2:
                st.subheader(row['Product_Name'])
                # 如果在搜尋狀態，顯示產品來源標籤
                if search_query:
                    st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
                st.write(row['Description'])
                st.link_button("View on Amazon", row['Affiliate_Link'])
            st.divider()

# 5. 主內容顯示邏輯
if search_query:
    # --- 模式 A: 全局搜尋 (無視分類，搜尋整張表) ---
    st.title(f"🔍 Results for: '{search_query}'")
    search_results = df[
        df['Product_Name'].str.contains(search_query, case=False, na=False) |
        df['Description'].str.contains(search_query, case=False, na=False)
    ]
    
    if search_results.empty:
        st.info("No matching products found across all collections.")
    else:
        render_item_list(search_results)

else:
    # --- 模式 B: 分類瀏覽 (原本的商品頁面) ---
    st.title(f"Explore: {main_page}")
    
    # 定義按鈕與 Excel 標籤的對應關係 (根據你的 Excel 內容)
    source_map = {
        "Toronto Base": "Toronto Base",
        "Amazon Top Choice": "Amazon Top Choice",
        "CC Picks": "CC Picks"
    }
    
    # 這裡解決了 NameError，我們使用字典取值
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    if page_df.empty:
        st.warning(f"No items found for {current_tag}.")
        st.write("Current Excel tags:", df[target_col].unique().tolist())
    else:
        # 自動根據該頁面現有的類別生成 Tabs
        unique_cats = page_df['Category'].unique().tolist()
        tabs = st.tabs(unique_cats)
        
        for i, cat in enumerate(unique_cats):
            with tabs[i]:
                cat_df = page_df[page_df['Category'] == cat]
                render_item_list(cat_df)
