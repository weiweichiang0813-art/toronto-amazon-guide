import streamlit as st
import pandas as pd

# ... 前面的 set_page_config 和 CSS 保持不變 ...

try:
    # 讀取 Excel
    df = pd.read_excel("my_products.xlsx")
    
    # 【關鍵修復 1】自動清理欄位名稱的空格
    df.columns = df.columns.str.strip()
    
    # 【關鍵修復 2】判斷你的 Excel 到底是用 'Source' 還是 'Sources'
    col_name = "Source" if "Source" in df.columns else "Sources"
    
    # 側邊欄選項 (確保與你最新 Excel 裡的內容一致)
    with st.sidebar:
        st.title("📍 Navigation")
        main_page = st.radio(
            "Select Collection",
            ["Toronto Base", "Amazon Top Choice", "CC Picks"],
            index=0
        )
        search_keyword = st.text_input("🔍 Search Products")

    # 過濾資料
    page_df = df[df[col_name] == main_page]

    if page_df.empty:
        st.warning(f"目前在 '{col_name}' 欄位中找不到與 '{main_page}' 完全匹配的資料。")
        st.info("請檢查 Excel 內容，例如 'CC Picks' 是否多打了一個空格。")
    else:
        # 顯示產品邏輯...
        categories = page_df['Category'].unique().tolist()
        tabs = st.tabs(categories)
        # ... 後續渲染循環 ...

except Exception as e:
    st.error(f"Error loading file: {e}")
