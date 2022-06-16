
import streamlit as st
import pandas as pd
import plotly.express as px

def backtest_dashboard(backtest_data_path):
    backtest_result = pd.read_csv(backtest_data_path)
    st.markdown("<h1 style='text-align: center;'>Backtest Results</h1>", unsafe_allow_html=True)

    #model filter
    model_list = backtest_result['model'].unique()
    selected_model = st.selectbox("Select Model",model_list)

    placeholder = st.empty()

    with placeholder.container():
        data = backtest_result[backtest_result['model'] == selected_model].round(decimals = 2)
        m1,m2,m3 = st.columns(3)

        m1.metric(label="Explained Variance", value=data['Explained Variance'].iloc[-1])
        m2.metric(label="MAE", value=data['MAE'].iloc[-1])
        m3.metric(label="MSE", value=data['MSE'].iloc[-1])  

        st.text("")

        m4,m5,m6 = st.columns(3)

        m4.metric(label="MedAE", value=data['MedAE'].iloc[-1])
        m5.metric(label="RSQ", value=data['RSQ'].iloc[-1])
        m6.metric(label="MAPE", value=data['MAPE'].iloc[-1]) 

        st.markdown("### MAPE Over Time")
        fig = px.line(data.iloc[-30:],x = 'date',y='MAPE')
        st.plotly_chart(fig, use_container_width=True)






