import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 2. 專業 CSS 樣式：美化背景、文字、按鈕、搜尋欄與 Top Bar
st.markdown("""
    <style>
    /* 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6 !important;
    }

    /* --- 1. 修改最上方 Top Bar (stHeader) 為白色 --- */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    /* --- 2. 側邊欄：白色背景 + 純黑文字 --- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 強制側邊欄內所有標籤、標題、一般文字為純黑色 */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* --- 3. 搜尋欄位美化：徹底解決撞色問題 --- */
    /* 強制搜尋框背景為純白色，文字為純黑色 */
    div[data-testid="stSidebar"] .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
    }
    /* 修改搜尋框提示文字 (Placeholder) 顏色 */
    div[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #888888 !important;
    }

    /* --- 4. 主內容區文字黑化 --- */
    .main h1, .main h2, .main h3, .main [data-testid="stHeader"], .main p, .main span, .main div {
        color: #000000 !important;
    }

    /* --- 5. 產品卡片美化 --- */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }

    /* --- 6. 亞馬遜橘色按鈕 (不變色) --- */
    .stLinkButton > a {
        background-color: #FF9900 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 12px 35px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .stLinkButton > a:hover {
        background-color: #e68a00 !important;
        transform: scale(1.02);
    }

    /* 圖片顯示限制 */
    .stImage img {
        max-height: 180px; /* 限制圖片高度 */
        width: auto;
        object-fit: contain;
        border-radius: 1
