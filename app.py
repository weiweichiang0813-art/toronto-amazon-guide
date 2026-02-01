import streamlit as st
import pandas as pd

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🔍", layout="wide")

# 2. 側邊欄導航 (對應你的 Excel Sources 欄位)
with st.sidebar:
    st.title("📍 Navigation")
    # 這裡的選項要跟 Excel 裡的 "Sources" 內容對應
    main_page = st.radio(
        "Select Collection",
        ["Toronto", "Amazon", "CC"], 
        index=0
    )
    search_keyword = st.text_input("🔍 Search Products", placeholder="e.g. Yoga")

# 3. 讀取與過濾數據
try:
    df = pd.read_excel("my_products.xlsx")
    
    # 根據側邊欄選取的 Source 過濾
    page_df = df[df['Sources'] == main_page]

    st.title(f"Collection: {main_page}")

    # 4. 動態建立 Tabs (根據你 Excel 實際有的 Category 自動生成)
    # 這樣如果你以後加了 "Shoes"，它會自動跑出來
    categories = page_df['Category'].unique().tolist()
    if not categories:
        st.warning("No categories found for this source.")
    else:
        tabs = st.tabs(categories)

        for i, cat in enumerate(categories):
            with tabs[i]:
                cat_df = page_df[page_df['Category'] == cat]
                
                # 搜尋過濾
                if search_keyword:
                    cat_df = cat_df[cat_df['Product_Name'].str.contains(search_keyword, case=False)]

                for _, row in cat_df.iterrows():
                    with st.container():
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            # 假設你的圖片放在 GitHub 的 images 資料夾
                            st.image(row['Image_URL'], use_container_width=True)
                        with col2:
                            st.subheader(row['Product_Name'])
                            st.write(row['Description'])
                            st.link_button("View on Amazon", row['Affiliate_Link'])
                        st.divider()

except Exception as e:
    st.error(f"Error loading file: {e}")
