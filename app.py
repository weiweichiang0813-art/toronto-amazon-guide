import streamlit as st
import pandas as pd

# 1. 網頁基礎配置
st.set_page_config(page_title="CC Picks the World", page_icon="🔍", layout="wide")

# 2. 專業 CSS 樣式
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .product-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    .stLinkButton>a {
        background-color: #FF9900 !important;
        color: white !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍Top Fashion Bestsellers in Toronto")
st.write("Handpicked from Amazon Canada's top-selling fashion essentials.")

# 3. 讀取數據 (確保你已將 Excel 上傳到 GitHub)
try:
    df = pd.read_excel("my_products.xlsx")
    
    for index, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2], gap="medium")
            with col1:
                # 這裡會讀取你上傳到 GitHub 的圖片
                st.image(row['Image_URL'], use_container_width=True)
            with col2:
                st.header(row['Product_Name'])
                st.write(f"**Category:** {row['Category']}")
                st.write(row['Description'])
                st.link_button("View on Amazon.ca", row['Affiliate_Link'])
            st.divider()

except Exception as e:
    st.error("Please make sure 'my_products.xlsx' is uploaded to your GitHub repository.")
    st.info("Check if you have added 'pandas' and 'openpyxl' to your requirements.txt")

st.caption("As an Amazon Associate, I earn from qualifying purchases.")


