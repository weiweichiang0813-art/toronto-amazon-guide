import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 專業 CSS 樣式：移除 Banner、美化側邊欄與產品卡片
st.markdown("""
    <style>
    /* 1. 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6;
    }

    /* 2. 側邊欄專屬樣式：白色背景 + 黑色文字 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 強制側邊欄內所有文字（標題、標籤、按鈕文字）為黑色 */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }

    /* 3. 搜尋欄位美化：確保在白色側邊欄內清晰 */
    .stTextInput input {
        background-color: #f9f9f9 !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }

    /* 4. 產品卡片美化：純白背景 + 陰影 */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }

    /* 5. 亞馬遜橘色按鈕 */
    .stLinkButton > a {
        background-color: #FF9900 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stLinkButton > a:hover {
        background-color: #e68a00 !important;
        color: #ffffff !important;
    }

    /* 6. 主內容區文字顏色：深色確保易讀 */
    .main h1, .main h2, .main h3, .main p, .main span {
