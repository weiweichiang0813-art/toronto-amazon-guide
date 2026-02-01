import streamlit as st
import pandas as pd

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 讀取與清理數據
try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip() # 清除標題空格
    
    # 兼容你的 Excel 欄位名稱 (Sources 或 Source)
    target_col = "Sources" if "Sources" in df.columns else "Source"
    
    # 清除內容空格，確保 "Toronto " 變回 "Toronto"
    df[target_col] = df[target_col].astype(str).str.strip()
    df['Category'] = df['Category'].astype(str).str.strip()
    
except Exception as e:
    st.error(f"無法讀取 Excel 檔案: {e}")
    st.stop()

# 3. 側邊欄導航
with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Top Choice", "CC Picks"],
        index=0
    )
    # 搜尋框
    search_query = st.text_input("🔍 Search ALL Products", placeholder="Try searching 'Yoga'...")

# 4. 產品顯示函數 (統一風格)
def render_products(data_to_show):
    for _, row in data_to_show.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row['Image_URL'], use_container_width=True)
            with col2:
                st.subheader(row['Product_Name'])
                # 搜尋時額外顯示它在哪個分類
                if search_query:
                    st.caption(f"Found in: {row[target_col]} | Category: {row['Category']}")
                st.write(row['Description'])
                st.link_button("View on Amazon", row['Affiliate_Link'])
            st.divider()

# 5. 主要顯示邏輯
if search_query:
    # --- 全局搜尋模式 ---
    st.title(f"🔍 Search Results for: '{search_query}'")
    results = df[
        df['Product_Name'].str.contains(search_query, case=False, na=False) |
        df['Description'].str.contains(search_query, case=False, na=False)
    ]
    
    if results.empty:
        st.info("No products found across any collection.")
    else:
        render_products(results)

else:
    # --- 原本的分頁模式 ---
    st.title(f"Explore: {main_page}")
    
    # 【關鍵對應】建立網頁按鈕與 Excel 簡寫的橋樑
    # 根據你 image_0738e1.png 的內容來對應
    source_map = {
        "Toronto Base": "Toronto",
        "Amazon Top Choice": "Amazon",
        "CC Picks": "CC"
    }
    
    # 取得 Excel 裡的簡寫
    excel_tag = source
