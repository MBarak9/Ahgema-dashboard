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

st.title("SALES PERFORMANCE")

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
    st.metric("Forecast accuracy", f"58 %")
# Fill rate
with col3 :
    current_month_fill_rate = df1.loc["Taux de service",selected_month]*100
    previous_month_fill_rate = 100*df1.loc["Taux de service",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta = round((current_month_fill_rate - previous_month_fill_rate)*100/previous_month_fill_rate,1)
    st.metric("Fill rate", f" {current_month_fill_rate:.0f} %",f"{delta}% MOM")
# Claims
with col4 :
    current_month_claims = df1.loc["Nb of Claims (Customers)",selected_month]
    previous_month_claims = df1.loc["Nb of Claims (Customers)",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]
    delta =current_month_claims - previous_month_claims
    st.metric("Customers Claims", f" {df1.loc['Nb of Claims (Customers)',selected_month]:,.0f}",f"{delta} MOM", "inverse")

# OTD
with col5 :
    current_month_otd = df1.loc["Customers OTD",selected_month]*100
    previous_month_otd = df1.loc["Customers OTD",df1.columns[max(0,df1.columns.get_loc(selected_month)-1)]]*100
    delta = round((current_month_otd - previous_month_otd)*100/previous_month_otd,1)
    st.metric("Ontime delivery", f" {df1.loc['Customers OTD',selected_month]*100:,.0f} %",f"{delta}% MOM")



# Order intake order backlog
order_data = df1.loc[["Sales","Order intake", "OrderBacklog"]].transpose()
order_data.columns = ["Sales","Order intake", "OrderBacklog"]
fig_order = px.bar(
    order_data,
    x=order_data.index,
    y=["Sales","Order intake", "OrderBacklog"],
    title="Sales vs Order Intake vs Order Backlog",
    labels={"index": "", "value": "Valeur en K€", "variable": "Légende"},
    barmode='group'
)
fig_order.update_layout( title_font_size=24) # Spécifiez la taille du titre ici
st.plotly_chart(fig_order, use_container_width=True)


# Columns
col1, col2 = st.columns(2)
#--- Credit notes ---
cn_data = df1.loc["Credit notes"].reset_index()

fig_cn = px.bar(
    cn_data,
    x="index",
    y="Credit notes",
    title="Credit notes by month",
    text=cn_data["Credit notes"].apply(lambda x: f"{x:.2f}K€"),  # add value labels

)
fig_cn.update_traces(textfont_size=20)
fig_cn.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=False,
    title_font_size=24
)
col1.plotly_chart(fig_cn, use_container_width=True)