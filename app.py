# --- 數據處理邏輯 (適配你的截圖) ---
try:
    df = pd.read_excel("my_products.xlsx")
    
    # 對應你的側邊欄按鈕與 Excel 裡的 Sources 簡寫
    # 如果按鈕選 "Toronto Base"，我們去 Excel 找 "Toronto"
    source_map = {
        "Toronto Base": "Toronto",
        "Amazon Top Choice": "Amazon",
        "CC Picks": "CC"
    }
    
    selected_source_code = source_map[main_page]
    
    # 這裡使用 'Sources' 因為你的截圖標題是這個
    page_df = df[df['Sources'] == selected_source_code]

    if page_df.empty:
        st.warning(f"No products found for {main_page} in the Excel file.")
    else:
        # 動態抓取該分類下的 Category (例如 Accessories, Clothing, Shoes)
        categories = page_df['Category'].unique().tolist()
        tabs = st.tabs(categories)

        for i, cat in enumerate(categories):
            with tabs[i]:
                # 過濾出該分類的產品
                cat_df = page_df[page_df['Category'] == cat]
                
                # 搜尋過濾
                if search_keyword:
                    cat_df = cat_df[cat_df['Product_Name'].str.contains(search_keyword, case=False)]

                for _, row in cat_df.iterrows():
                    with st.container():
                        st.markdown('<div class="product-box">', unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 2], gap="large")
                        with col1:
                            # 確保你的圖片檔案放在與 .py 檔同一個資料夾
                            st.image(row['Image_URL'], use_container_width=True)
                        with col2:
                            st.subheader(row['Product_Name'])
                            st.write(row['Description'])
                            st.link_button("View Details on Amazon", row['Affiliate_Link'])
                        st.markdown('</div>', unsafe_allow_html=True)

except KeyError as e:
    st.error(f"欄位名稱錯誤：請檢查 Excel 標題是否為 'Sources'。錯誤資訊: {e}")
except Exception as e:
    st.error(f"讀取檔案失敗: {e}")
