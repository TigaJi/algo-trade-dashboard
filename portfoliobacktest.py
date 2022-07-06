
import streamlit as st
import pandas as pd
import plotly.express as px

def portfolio_backtest_dashboard(portfolio_result):

    st.markdown("<h1 style='text-align: center;'>Portfolio Backtest Results</h1>", unsafe_allow_html=True)


    placeholder = st.empty()

    with placeholder.container():
        
        m1,m2,m3 = st.columns(3)

        m1.metric(label="EXP3", value=(portfolio_result['exp3'].iloc[-1]-10000)/10000)
        m2.metric(label="BAH", value=(portfolio_result['bah'].iloc[-1]-10000)/10000)
        m3.metric(label="CRP", value=(portfolio_result['crp'].iloc[-1]-10000)/10000)  

        st.text("")

        st.markdown("### Daily Backtest Result")
        fig = px.line(portfolio_result,y=["exp3","bah","crp"],showlegend = True)
        st.plotly_chart(fig, use_container_width=True)






