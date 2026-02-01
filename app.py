import streamlit as st
import pandas as pd

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 讀取與清理數據
try:
    df = pd.read_excel("my_products.xlsx")
    
    # 【自動修正 1】刪除欄位名稱前後的空白
    df.columns = df.columns.str.strip()
    
    # 【自動修正 2】相容你的 Source 或 Sources 欄位
    target_col = "Source" if "Source" in df.columns else "Sources"
    
    # 【自動修正 3】刪除內容裡面的空白 (例如把 "Toronto Base " 變成 "Toronto Base")
    df[target_col] = df[target_col].astype(str).str.strip()
    df['Category'] = df['Category'].astype(str).str.strip()

    # 3. 側邊欄導航
    with st.sidebar:
        st.title("📍 Navigation")
        # 這裡的選項必須跟 Excel 裡的內容完全一樣
        main_page = st.radio(
            "Select Collection",
            ["Toronto Base", "Amazon Top Choice", "CC Picks"],
            index=0
        )
        search_query = st.text_input("🔍 Search Products")

    # 4. 過濾數據
    page_df = df[df[target_col] == main_page]

    # --- 偵錯顯示 (如果還是沒東西，這行會告訴你原因) ---
    if page_df.empty:
        st.warning(f"找不到匹配 '{main_page}' 的資料。")
        st.write("Excel 內現有的標籤有：", df[target_col].unique())
    else:
        st.title(f"Explore: {main_page}")
        
        # 5. 分類 Tabs
        categories = page_df['Category'].unique().tolist()
        tabs = st.tabs(categories)

        for i, cat in enumerate(categories):
            with tabs[i]:
                cat_df = page_df[page_df['Category'] == cat]
                
                # 搜尋過濾
                if search_query:
                    cat_df = cat_df[cat_df['Product_Name'].str.contains(search_query, case=False)]

                for _, row in cat_df.iterrows():
                    with st.container():
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            # 顯示圖片
                            st.image(row['Image_URL'], use_container_width=True)
                        with c2:
                            st.subheader(row['Product_Name'])
                            st.write(row['Description'])
                            st.link_button("View on Amazon", row['Affiliate_Link'])
                        st.divider()

except Exception as e:
    st.error(f"讀取檔案失敗: {e}")
