import streamlit as st
import pandas as pd 
import numpy as numpy
import time
import plotly.express as px
#a function to format the transaction data
#extract data and kept only recent 5 transcations
#rename columns for better format


def realtime_dashboard(portfolio_value, transactions):
    #Page title
    st.markdown("<h1 style='text-align: center;'>Real Time Results</h1>", unsafe_allow_html=True)
    st.text("Last updated: "+portfolio_value['dt'].iloc[-1])
    graph_filter = st.selectbox("Select Graph",['value','return'])
    

    #single element container
    placeholder = st.empty()




    day_return =  portfolio_value['daily_return'].iloc[-1]
    week_return =  portfolio_value['weekly_return'].iloc[-1]
    month_return =  portfolio_value['monthly_return'].iloc[-2]

        
    with placeholder.container():

        m1, m2, m3 = st.columns(3)

        m1.metric(label="Daily Return", value=str(day_return*100)+"%")
        m2.metric(label="Weekly Return", value=str(week_return*100)+"%")
        m3.metric(label="Monthly Return", value=str(month_return*100)+"%")


        st.markdown("### Portfolio " + graph_filter)
        fig = px.line(portfolio_value.iloc[-20:],y=graph_filter)
        st.plotly_chart(fig, use_container_width=True)

        box1,box2 = st.columns(2)
        with box1:
            st.markdown("### Basket")

            basket_df = transactions.groupby(['yahoo_ticker'])[['total_shares_held']].last().reset_index()
            basket_df = basket_df.loc[basket_df['total_shares_held'] > 0]
            box1.dataframe(basket_df, width = 300,height= 3000)
        with box2:
            st.markdown("### Transactions")
            box2.table(transactions[['date','action','company','num_shares','total_usd']].tail(5).astype(str))
        
