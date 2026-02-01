import streamlit as st
import pandas as pd

# 1. 讀取與清理數據 (增加 strip 確保匹配準確)
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    # 這裡兼容你 Excel 裡的 'Sources' 或 'Source'
    target_col = "Sources" if "Sources" in df.columns else "Source"
    df[target_col] = df[target_col].astype(str).str.strip()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# 2. 側邊欄導航
with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio("Select Collection", ["Toronto Base", "Amazon Top Choice", "CC Picks"])
    # 這是你的搜尋框
    search_query = st.text_input("🔍 Search ALL Products", placeholder="Type to search everything...")

# 3. 主頁面邏輯
if search_query:
    # --- 全局搜尋模式 ---
    st.title(f"🔍 Search Results for: '{search_query}'")
    
    # 從整個 df 中尋找 (不分 Source, 不分 Category)
    search_results = df[
        df['Product_Name'].str.contains(search_query, case=False, na=False) |
        df['Description'].str.contains(search_query, case=False, na=False)
    ]
    
    if search_results.empty:
        st.info("No products found across all collections.")
    else:
        st.write(f"Found {len(search_results)} items:")
        # 直接渲染搜尋到的結果
        for _, row in search_results.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1: st.image(row['Image_URL'], use_container_width=True)
                with c2:
                    st.subheader(row['Product_Name'])
                    st.caption(f"Location: {row[target_col]} | Category: {row['Category']}")
                    st.write(row['Description'])
                    st.link_button("View on Amazon", row['Affiliate_Link'])
                st.divider()
else:
    # --- 常規分頁模式 (你原本的邏輯) ---
    st.title(f"Explore: {main_page}")
    
    # 根據你的 Excel 簡寫進行對應
    source_map = {"Toronto Base": "Toronto", "Amazon Top Choice": "Amazon", "CC Picks": "CC"}
    filtered_df = df[df[target_col] == source_map[main_page]]
    
    if filtered_df.empty:
        st.warning("No items found for this collection.")
    else:
        # 動態生成 Tabs
        categories = filtered_df['Category'].unique().tolist()
        tabs = st.tabs(categories)
        for i, cat in enumerate(categories):
            with tabs[i]:
                cat_items = filtered_df[filtered_df['Category'] == cat]
                for _, row in cat_items.iterrows():
                    # ... 渲染商品代碼 ...
                    st.subheader(row['Product_Name'])
                    st.image(row['Image_URL'], width=300)
                    st.write(row['Description'])
                    st.link_button("View on Amazon", row['Affiliate_Link'])
                    st.divider()
