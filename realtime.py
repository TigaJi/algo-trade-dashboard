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
    st.text("Last update on: "+transactions['date'].iloc[-1])
    graph_filter = st.selectbox("Select Graph",['profit_sum','return'])
    
    #hide index
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    #single element container
    placeholder = st.empty()

    day_return =  portfolio_value['daily_return'].iloc[-1]
    week_return =  portfolio_value['weekly_return'].iloc[-1]
    month_return =  portfolio_value['monthly_return'].iloc[-1]

        
    with placeholder.container():

        m1, m2, m3 = st.columns(3)

        m1.metric(label="Daily Return", value=round(day_return,4))
        m2.metric(label="Weekly Return", value=round(week_return,4))
        m3.metric(label="Monthly Return", value=round(month_return,4))


        st.markdown("### Portfolio " + graph_filter)
        fig = px.line(portfolio_value[-100:],y=graph_filter)
        st.plotly_chart(fig, use_container_width=True)

        box1,box2 = st.columns(2)
        with box1:
            st.markdown("### Basket")

            basket_df = transactions.groupby(['yahoo_ticker'])[['total_shares_held']].last().reset_index()
            basket_df_1 = basket_df.loc[basket_df['total_shares_held'] > 0]
            basket_df_1['total_shares_held'] = basket_df_1['total_shares_held'].astype(int)
            box1.table(basket_df_1)

        with box2:
            st.markdown("### Transactions")
            transactions['total_usd'] = transactions['total_usd'].round(2)
            transactions['num_shares'] = transactions['num_shares'].astype(int)
            box2.table(transactions[['date','action','company','num_shares','total_usd']].tail(5).astype(str))
        
