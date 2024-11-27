import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# --- LOAD CSS ---  
css_path = pathlib.Path(__file__).parent.parent / "assets" / "style.css"
load_css(css_path)

st.title("PROCUREMENT PERFORMANCE")

# --- LOAD THE DATA AND TRANSFORM ---
# Vérifier si les données sont disponibles dans st.session_state
if 'df1' in st.session_state:
    df1 = st.session_state['df1']
    # Utiliser les données pour créer des graphiques ou autres analyses
else:
    st.warning("No data available. Please upload an Excel file on the import page.")
    st.stop()

# --- FILTRES ---
selected_month = st.sidebar.selectbox("Select a month :", df1.columns)

# --- Section 1 : Cartes KPI ---
col1, col2, col3, col4 = st.columns(4,gap="small")

# Total purchase
with col1 :
    current_month_purchasing = df1.loc["Purchasing",selected_month]
    previous_month_purchasing = df1.loc["Purchasing",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_purchasing - previous_month_purchasing) * 100/previous_month_purchasing,1)
    st.metric(label="Total Purchases", value=f" {current_month_purchasing:,.0f}K€",delta=f"{delta}% MOM")
# Accuracy
with col2 :
    current_month_cost = df1.loc["Logistic cost",selected_month]+df1.loc["Purchasing",selected_month]
    previous_month_cost = df1.loc["Logistic cost",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]+df1.loc["Purchasing",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_cost - previous_month_cost) * 100/previous_month_cost,1)
    st.metric("Forecast accuracy", f"99 %")
# Pieces received
with col3 :
    current_month_fill_rate = df1.loc["Nb pieces received",selected_month]
    previous_month_fill_rate = df1.loc["Nb pieces received",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_fill_rate - previous_month_fill_rate)*100/previous_month_fill_rate,1)
    st.metric("Pieces received", f" {current_month_fill_rate:.0f} %",f"{delta}% MOM")
# Overdue pieces
with col4 :
    current_month_claims = df1.loc["Value of overdue pieces (Suppliers)",selected_month]
    previous_month_claims = df1.loc["Value of overdue pieces (Suppliers)",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta =current_month_claims - previous_month_claims
    st.metric("Value of overdue pieces", f" {df1.loc['Nb of Claims (Customers)',selected_month]:,.0f}",f"{delta} MOM", "inverse")


# Columns
col1, col2 = st.columns(2)
#--- Suppliers OTD ---
cn_data = df1.loc["Suppliers OTD"].reset_index()
cn_data["Suppliers OTD"] = cn_data["Suppliers OTD"]*100

fig_cn = px.line(
    cn_data,
    x="index",
    y="Suppliers OTD",
    title="Suppliers OTD by month",
    markers=True,
    text=cn_data["Suppliers OTD"].apply(lambda x: f"{x:.0f}%"),  # add value labels

)
fig_cn.update_traces(marker=dict(size=10), textposition="top center",textfont_size=14)
fig_cn.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=True,
    title_font_size=24,
    xaxis_title=""
)
col1.plotly_chart(fig_cn, use_container_width=True)

#--- Trnasport cost ---
cn_data = df1.loc["Transports costs (Purchasing)"].reset_index()

fig_cn = px.bar(
    cn_data,
    y="index",
    x="Transports costs (Purchasing)",
    title="Transports costs (Purchasing)",
    text=cn_data["Transports costs (Purchasing)"].apply(lambda x: f"{x:.2f}K€"),  # Utiliser le nom correct de la colonne
    orientation='h'
)

fig_cn.update_traces(textfont_size=20)
fig_cn.update_layout(
    yaxis=dict(showticklabels=True, title=''), 
    yaxis_showgrid=False,
    title_font_size=24,
    xaxis_title=""
)

col2.plotly_chart(fig_cn, use_container_width=True)

col1, col2 = st.columns(2)
#--- Stock value ---
cn_data = df1.loc["Inventory / Stock (value)"].reset_index()

fig_cn = px.bar(
    cn_data,
    y="index",
    x="Inventory / Stock (value)",
    title="Inventory value",
    text=cn_data["Inventory / Stock (value)"].apply(lambda x: f"{x:.0f}K€"),  # Utiliser le nom correct de la colonne
    orientation='h'
)

fig_cn.update_traces(textfont_size=20)
fig_cn.update_layout(
    yaxis=dict(showticklabels=True, title=''), 
    yaxis_showgrid=False,
    title_font_size=24,
    xaxis_title=""
)

col1.plotly_chart(fig_cn, use_container_width=True)

#--- Stock value ---
cn_data = df1.loc["Coût de stockage"].reset_index()

fig_cn = px.bar(
    cn_data,
    x="index",
    y="Coût de stockage",
    title="Possession Cost",
    text=cn_data["Coût de stockage"].apply(lambda x: f"{x:.1f}K€"),  # Utiliser le nom correct de la colonne
)

fig_cn.update_traces(textfont_size=20)
fig_cn.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=False,
    title_font_size=24,
    xaxis_title=""
)

col2.plotly_chart(fig_cn, use_container_width=True)
