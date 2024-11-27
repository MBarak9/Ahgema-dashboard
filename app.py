import streamlit as st
import numpy as np
import pandas as pd
import pathlib

# --- PAGES SETUP ---
st.set_page_config(layout="wide")

# --- FUNCTION TO LOAD CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# --- LOAD CSS ---  
css_path = pathlib.Path(__file__).parent / "assets" / "style.css"
load_css(css_path)

# --- ADD LOGO ---
st.logo("images/image.png", size="large")

# --- SIDEBAR AND PAGES ---
data_page = st.Page(
    page="views/data.py",
    title="📊Data"
)
overview_page = st.Page(
    page="views/overview.py",
    title="🏠Overview",
    default=True
)
sales_page = st.Page(
    page="views/sales.py",
    title="💰Sales"
)
purchasing_page = st.Page(
    page="views/purchasing.py",
    title="📦Procurement"
)
operations_page = st.Page(
    page="views/operations.py",
    title="👷Operations"
)
reverse_logistics_page = st.Page(
    page="views/reverse_logistics.py",
    title="♻️Reverse Logistics"
)
finance_page = st.Page(
    page="views/finance.py",
    title="💹Finance"
)

transport_page = st.Page(
    page="views/transport.py",
    title="🚚Transport"
)
# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation({"Data": [data_page], 
                    "Pages": [overview_page,sales_page,purchasing_page,operations_page ,transport_page,reverse_logistics_page, finance_page]
                    })

# --- RUN NAVIGATION ---
pg.run()



