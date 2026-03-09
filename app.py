import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

# -------------------- STYLE --------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
background: linear-gradient(135deg,#ffd6e8,#fff3e6);
}

h1{
text-align:center;
color:#d63384;
}

div[data-testid="metric-container"]{
background-color: rgba(255,255,255,0.85);
padding:15px;
border-radius:15px;
box-shadow:0px 6px 15px rgba(0,0,0,0.08);
}

.stPlotlyChart{
background-color:rgba(255,255,255,0.9);
padding:15px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("📊 Retail Sales Analytics Dashboard")

# -------------------- FILE UPLOAD --------------------
st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    np.random.seed(42)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    data = pd.DataFrame({
        "Month": months,
        "Sales": np.random.randint(2500,8000,12),
        "Profit": np.random.randint(500,2000,12),
        "Orders": np.random.randint(100,500,12),
        "Category": np.random.choice(["Electronics","Fashion","Home","Sports","Beauty"],12)
    })

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("🎛 Filters")

selected_month = st.sidebar.multiselect(
"Select Month",
options=data["Month"].unique(),
default=data["Month"].unique()
)

filtered_data = data[data["Month"].isin(selected_month)]

# -------------------- KPI METRICS --------------------
c1,c2,c3 = st.columns(3)

c1.metric("💰 Total Sales",f"${filtered_data['Sales'].sum()}")
c2.metric("📦 Total Orders",filtered_data['Orders'].sum())
c3.metric("📈 Total Profit",f"${filtered_data['Profit'].sum()}")

st.markdown("---")

# -------------------- CHART ROW 1 --------------------
col1,col2 = st.columns(2)

with col1:
    fig = px.line(
        filtered_data,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )
    st.plotly_chart(fig,use_container_width=True)

with col2:
    fig = px.bar(
        filtered_data,
        x="Month",
        y="Profit",
        color="Profit",
        title="Monthly Profit"
    )
    st.plotly_chart(fig,use_container_width=True)

# -------------------- CHART ROW 2 --------------------
col3,col4 = st.columns(2)

with col3:
    fig = px.scatter(
        filtered_data,
        x="Orders",
        y="Profit",
        size="Sales",
        color="Sales",
        title="Orders vs Profit"
    )
    st.plotly_chart(fig,use_container_width=True)

with col4:
    fig = px.histogram(
        filtered_data,
        x="Profit",
        nbins=10,
        title="Profit Distribution"
    )
    st.plotly_chart(fig,use_container_width=True)

# -------------------- HEATMAP --------------------
st.subheader("🔥 Correlation Analysis")

corr = filtered_data[["Sales","Profit","Orders"]].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdPu"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------- SALES FORECAST --------------------
st.subheader("🔮 Sales Forecast")

future_months = ["Next1","Next2","Next3"]

forecast_sales = list(filtered_data["Sales"].tail(3) + np.random.randint(100,500,3))

forecast_df = pd.DataFrame({
"Month":future_months,
"Sales":forecast_sales
})

forecast_plot = pd.concat([filtered_data[["Month","Sales"]],forecast_df])

fig = px.line(
forecast_plot,
x="Month",
y="Sales",
markers=True,
title="Predicted Sales Trend"
)

st.plotly_chart(fig,use_container_width=True)

st.success("Dashboard Loaded Successfully 🚀")