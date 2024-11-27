import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib

# --- FUNCTION TO LOAD CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- LOAD CSS ---  
css_path = pathlib.Path(__file__).parent.parent / "assets" / "style.css"
load_css(css_path)

# --- TITLE ---
st.title("GLOBAL PERFORMANCE")

# --- LOAD THE DATA AND TRANSFORM ---
# Vérifier si les données sont disponibles dans st.session_state
if 'df1' in st.session_state:
    df1 = st.session_state['df1']
    # Utiliser les données pour créer des graphiques ou autres analyses
else:
    st.warning("No data available. Please upload an Excel file on the import page.")
    st.stop()

# --- ADD ICON TO A METRIC ---

# --- FILTRES ---
selected_month = st.sidebar.selectbox("Select a month :", df1.columns)

# --- Section 1 : Cartes KPI ---
col1, col2, col3, col4, col5 = st.columns(5,gap="small")

# Total sales
with col1 :
    current_month_sales = df1.loc["Sales",selected_month]
    previous_month_sales = df1.loc["Sales",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_sales - previous_month_sales) * 100/previous_month_sales,1)
    # col1.markdown("<p style='font-size:24px; font-family:sans-serif; margin-bottom:0;'>Total Sales</p>", unsafe_allow_html=True)
    st.metric(label="Total Sales", value=f" {current_month_sales:,.0f}K€",delta=f"{delta}% MOM")
# Total Cost
with col2 :
    current_month_cost = df1.loc["Logistic cost",selected_month]+df1.loc["Purchasing",selected_month]
    previous_month_cost = df1.loc["Logistic cost",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]+df1.loc["Purchasing",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_cost - previous_month_cost) * 100/previous_month_cost,1)
    st.metric("Total Cost", f" {current_month_cost:,.0f}K€",f"{delta}% MOM","inverse")
# Fill rate
with col3 :
    current_month_fill_rate = df1.loc["Taux de service",selected_month]*100
    previous_month_fill_rate = 100*df1.loc["Taux de service",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_fill_rate - previous_month_fill_rate)*100/previous_month_fill_rate,1)
    st.metric("Fill rate", f" {current_month_fill_rate:.0f} %",f"{delta}% MOM")
# Inventory value
with col4 :
    current_inventory_value = df1.loc["Inventory / Stock (value)",selected_month]
    previous_inventory_value = df1.loc["Inventory / Stock (value)",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_inventory_value - previous_inventory_value)*100/previous_inventory_value,1)
    st.metric("Inventory value", f" {df1.loc['Inventory / Stock (value)',selected_month]:,.0f}K€",f"{delta}% MOM")
# Cash to Cash Cycle
with col5 :
    current_month_ccc = df1.loc["CCC",selected_month]
    previous_month_ccc = df1.loc["CCC",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_ccc - previous_month_ccc)*100/previous_month_ccc,1)
    st.metric("Cash to Cash Cycle", f" {df1.loc['CCC',selected_month]:,.0f} Days",f"{delta}% MOM")


# --- Section 2 : Visualsations ---
# Sales, Purchases, Logistic Cost 
s_p_l_data = df1.loc[["Sales", "Purchasing", "Logistic cost"]].transpose()
s_p_l_data.columns = ["Sales", "Purchases", "Logistic cost"]

fig_s_p_l = px.bar(
    s_p_l_data,
    x=s_p_l_data.index,
    y=["Sales", "Purchases", "Logistic cost"],
    title="Sales vs Purchases vs Logistic Cost",
    labels={"index": "", "value": "Valeur en K€", "variable": "Légende"},
    barmode='group'
)
fig_s_p_l.update_layout( title_font_size=24) # Spécifiez la taille du titre ici
st.plotly_chart(fig_s_p_l, use_container_width=True)

col1, col2, col3 = st.columns(spec=[0.5,0.25,0.25])

# Graphique : Claims in vertical bar chart
claims_data = df1.loc[["Nb of Claims (Customers)", "Nb of Claims (Suppliers)", "Nb of Claims (Transports)", "Nb of Claims (Quality)"], selected_month]
claims_data.index = ["Customers", "Suppliers", "Transports", "Quality"]
# Créer le bar chart avec Plotly
fig_claims = px.bar(
    claims_data,
    x=claims_data.index,
    y=selected_month,
    title=f"Number of Claims in {selected_month}",
    barmode='group',
    text=selected_month,
    orientation='v'
)
fig_claims.update_traces(textfont_size=20)
# Masquer les valeurs de l'axe y 
fig_claims.update_layout(yaxis=dict(showticklabels=False, title=""),
                         title_font_size=24,
                         yaxis_showgrid=False,
                         xaxis_title="")
# Afficher le graphique dans Streamlit
col1.plotly_chart(fig_claims, use_container_width=True)

# gauge chart for OTD

import plotly.graph_objects as go

# Suppliers OTD
current_s_otd = df1.loc["Suppliers OTD", selected_month]*100

fig_s_otd = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_s_otd,
    number = {'suffix': " %"},
    gauge = {
        'axis': {'range': [None, 100]},
        }))

fig_s_otd.update_layout(title="Suppliers OTD",title_font_size=24, title_x=0.25)
col2.plotly_chart(fig_s_otd)
# Customers OTD
current_c_otd = df1.loc["Customers OTD", selected_month]*100

fig_c_otd = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_c_otd,
    number = {'suffix': " %"},
    gauge = {
        'axis': {'range': [None, 100]},
        }
))

fig_c_otd.update_layout(title="Customers OTD",title_font_size=24, title_x=0.25)
col3.plotly_chart(fig_c_otd)

col1, col2 = st.columns(2)

# --- Inventory turnover by month ---
turnover_df = df1.loc["Inventory turns /Rotation"]

fig_turn = px.line(turnover_df, title="Inventory turnover by month", 
                   markers=True,
                   text=turnover_df)

fig_turn.update_traces(marker=dict(size=10), text=turnover_df, textposition="top center")
fig_turn.update_layout(
    title_font_size=24,  # Spécifiez la taille du titre ici
    yaxis=dict(showticklabels=False, title=''),  # Masquer les valeurs de l'axe y et le titre de l'axe y
    yaxis_showgrid=False,  # Enlever la grille de l'axe y
    xaxis_title="",  # Masquer le titre de l'axe x
    showlegend=False
)

# Afficher le graphique dans Streamlit
col1.plotly_chart(fig_turn, use_container_width=True)

# --- DPO and DSO ---

dpo_dso_data = df1.loc[["DPO", "DSO"]].transpose()
dpo_dso_data.columns = ["DPO", "DSO"]

fig_dpo_dso = px.bar(
    dpo_dso_data,
    x=dpo_dso_data.index,
    y=["DPO", "DSO"],
    title="DPO vs DSO",
    labels={"index": "", "value": "Valeur en K€", "variable": "Légende"},
    barmode='group'
)
fig_dpo_dso.update_layout( title_font_size=24) # Spécifiez la taille du titre ici
col2.plotly_chart(fig_dpo_dso, use_container_width=True)  
