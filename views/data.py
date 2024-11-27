import streamlit as st
import pandas as pd
import pathlib

# --- FUNCTION TO LOAD CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# --- LOAD CSS ---  
css_path = pathlib.Path(__file__).parent.parent / "assets" / "style.css"
load_css(css_path)

# --- TITLE ---
st.title("IMPORT EXCEL FILE")

# --- DATA UPLOADER ---
uploaded_file = st.file_uploader("Upload your Excel file")

if uploaded_file is not None:
    # --- LOAD THE DATA AND TRANSFORM ---
    data = pd.ExcelFile(uploaded_file)
    report1_df = data.parse("Report 1")
    df1 = report1_df[report1_df.columns[1:14]].set_index("Metric") # df1 = df of report 1
    nb_of_valid_months = df1.loc["Sales"].count()
    df1 = df1[df1.columns[:nb_of_valid_months]]

    report2_df = data.parse("Report 2")
    df2 = report2_df[report2_df.columns[0:14]].set_index("Incoterms") # df1 = df of report 1
    nb_of_valid_months = df2.loc["EXW"].count()
    df2 = df2[df2.columns[:nb_of_valid_months]]



    # Stocker les données dans st.session_state
    st.session_state['file'] = uploaded_file
    st.session_state['df1'] = df1
    st.session_state['df2'] = df2

    # Afficher les données pour vérification
    st.write(df1)
    st.write(df2)
else:
    # Vérifier si les données existent déjà dans st.session_state
    if 'df1' in st.session_state:
        df1 = st.session_state['df1']
        df2 = st.session_state['df2']
        file = st.session_state['file']
        st.write(f"Le fichier actuellement importé est '{file.name}'")
        st.write(df1)
        st.write(df2)
    else:
        st.warning("Please upload an Excel file.")
