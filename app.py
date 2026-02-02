import streamlit as st
import pandas as pd
import os

# 1. 網頁配置
st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

# 初始化 Session State 用於管理搜尋紀錄
if 'search_val' not in st.session_state:
    st.session_state.search_val = ""

# 定義切換分類時清空搜尋的函數
def clear_search():
    st.session_state.search_val = ""

# 2. 專業 CSS 樣式：調整深咖啡色 Tabs 與文字黑化
st.markdown("""
    <style>
    /* 全網頁背景：淺灰色 */
    .stApp {
        background-color: #f4f7f6 !important;
    }

    /* 1. 修改最上方 Top Bar 為白色 */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    /* 2. 側邊欄：白色背景 + 純黑文字 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 3. 搜尋欄位：白底黑字 */
    div[data-testid="stSidebar"] .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #d0d0d0 !important;
        border-radius: 8px !important;
    }

    /* 4. 強制主內容區所有級別標題與文字變黑 (解決 Explore 看不見的問題) */
    .main h1, .main h2, .main h3, h1, h2, h3, .main p, .main span, .main div {
        color: #000000 !important;
        font-weight: 500;
    }
    h1 { font-weight: 800 !important; }

    /* 5. 產品卡片 */
    .product-box {
        background-color: #ffffff !important;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }

    /* 6. 亞馬遜橘色按鈕 */
    .stLinkButton > a {
        background-color: #FF9900 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 12px 35px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
    }

    /* 7. 分類 Tabs 樣式修改：改為深咖啡色 */
    .stTabs [data-baseweb="tab"] {
        color: #444444 !important; /* 未選中時的顏色 */
        font-weight:
