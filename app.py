import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CC Picks the World", page_icon="🌎", layout="wide")

if 'search_val' not in st.session_state:
    st.session_state.search_val = ""

def clear_search():
    st.session_state.search_val = ""

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6 !important; }

    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
        border-bottom: 1px solid #e0e0e0;
    }
    header[data-testid="stHeader"] * {
        color: #000000 !important;
        fill: #000000 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stSidebar"] .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #d0d0d0 !important;
    }

    .main h1, h1 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    .main h3, h3 {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    .product-box p, .product-box div, .main p, [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 400 !important; /* 恢復為 Normal */
        line-height: 1.6;
    }

    .product-box {
        background-color: #ffffff !important;
        padding: 25px; margin-bottom: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #eef0f2;
    }
    .stLinkButton > a {
        background-color: #A68966 !important; 
        color: #ffffff !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 10px 30px !important;
        text-decoration: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #444444 !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #5D4037 !important;
        border-bottom: 3px solid #3E2723 !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: transparent !important;
    }

    .stImage img { max-height: 180px; width: auto; object-fit: contain; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = pd.read_excel("my_products.xlsx")
    df.columns = df.columns.str.strip()
    target_col = "Source" if "Source" in df.columns else "Sources"
    for col in [target_col, 'Category', 'Product_Name', 'Image_URL']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
except Exception as e:
    st.error(f"Excel 讀取失敗: {e}"); st.stop()

with st.sidebar:
    st.title("📍 Navigation")
    main_page = st.radio(
        "Select Collection",
        ["Toronto Base", "Amazon Choice", "CC Picks"],
        index=0,
        on_change=clear_search
    )
    search_query = st.text_input(
        "🔍 Search ALL Products", 
        placeholder="Search anything...",
        key="search_val"
    )

def render_item_list(data):
    for _, row in data.iterrows():
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4]) 
        with col1:
            img_path = f"image/{row['Image_URL']}"
            
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning(f"⚠️ 圖片檔名不符: {row['Image_URL']}")
            # ----------------------
            
        with col2:
            st.subheader(row['Product_Name'])
            if st.session_state.search_val:
                st.caption(f"Source: {row[target_col]} | Category: {row['Category']}")
            
            st.write(row['Description'])
            st.link_button("View on Amazon", row['Affiliate_Link'])
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.search_val:
    st.title(f"🔍 Results: '{st.session_state.search_val}'")
    results = df[df['Product_Name'].str.contains(st.session_state.search_val, case=False, na=False) | 
              df['Description'].str.contains(st.session_state.search_val, case=False, na=False)]
    if results.empty:
        st.info("No matching products found.")
    else:
        render_item_list(results)
else:
    st.title(f"Explore: {main_page}")
    source_map = {"Toronto Base": "Toronto Base", "Amazon Choice": "Amazon Choice", "CC Picks": "CC Picks"}
    current_tag = source_map.get(main_page)
    page_df = df[df[target_col] == current_tag]
    
    if page_df.empty:
        page_df = df[df[target_col] == main_page.split()[0]]

    if not page_df.empty:
        unique_cats = page_df['Category'].unique().tolist()
        tabs = st.tabs(unique_cats)
        for i, cat in enumerate(unique_cats):
            with tabs[i]:
                render_item_list(page_df[page_df['Category'] == cat])
    else:
        st.warning(f"No items found for {main_page}.")

st.divider()
st.caption("© 2026 CC Picks the World | As an Amazon Associate, I earn from qualifying purchases.")




