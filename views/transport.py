import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib

# --- FUNCTION TO LOAD CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# --- LOAD CSS ---  
css_path = pathlib.Path(__file__).parent.parent / "assets" / "style.css"
load_css(css_path)

st.title("TRANSPORT PERFORMANCE")

# --- LOAD THE DATA AND TRANSFORM ---
# Vérifier si les données sont disponibles dans st.session_state
if 'df1' in st.session_state:
    df1 = st.session_state['df1']
    df2 = st.session_state['df2']
    # Utiliser les données pour créer des graphiques ou autres analyses
else:
    st.warning("No data available. Please upload an Excel file on the import page.")
    st.stop()

# --- FILTRES ---
selected_month = st.sidebar.selectbox("Select a month :", df2.columns)

# --- Section 1 : Incoterms ---
current_inco = df2.iloc[:10,df2.columns.get_loc(selected_month)]
fig_inco = px.bar(current_inco, 
                  x=current_inco.index,
                  y=current_inco.values,
                  text=current_inco.values,
                  title=f"Incoterms used in {selected_month}")

fig_inco.update_traces(textfont_size=20)
fig_inco.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=False,
    title_font_size=24
)
st.plotly_chart(fig_inco, use_container_width=True)

# --- Section 2 : Non maitrise des transports ---
nmt = df2.loc["EXW _FCA_FOB / TOTAL"].reset_index()
nmt["EXW _FCA_FOB / TOTAL"] = nmt["EXW _FCA_FOB / TOTAL"]*100
fig_nmt = px.bar(nmt, 
                  x="index",
                  y="EXW _FCA_FOB / TOTAL",
                  text=nmt['EXW _FCA_FOB / TOTAL'].apply(lambda x: f"{x:.0f}%"),
                  title="Non maitrise de transport (EXW-FCA-FOB)")

fig_nmt.update_traces(textfont_size=20)
fig_nmt.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=False,
    title_font_size=24,
    xaxis_title=""
)
st.plotly_chart(fig_nmt, use_container_width=True)

# --- Section 3 : Transport cost en barres empilé ---
cost = df1.loc[["Transports costs (Purchasing)","Transports costs (Sales)"]].reset_index().melt(id_vars='Metric', var_name='Month', value_name='Value')
print(cost)
fig_cost = px.bar( cost, x='Month', 
                  y='Value', 
                  color='Metric', 
                  title='Transports Costs by Month',
                  text=cost["Value"].apply(lambda x: f"{x:,.0f} K€"),
                  barmode='stack' )

fig_cost.update_traces(textfont_size=20)
fig_cost.update_layout(
    yaxis=dict(showticklabels=False, title=''), 
    yaxis_showgrid=False,
    title_font_size=24,
    xaxis_title=""
)
st.plotly_chart(fig_cost, use_container_width=True)