
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly

def portfolio_backtest_dashboard(portfolio_result):

    print(portfolio_result[100:110])
    st.markdown("<h1 style='text-align: center;'>Portfolio Backtest Results</h1>", unsafe_allow_html=True)


    placeholder = st.empty()

    with placeholder.container():
        
        m1,m2,m3 = st.columns(3)

        m1.metric(label="EXP3", value=round((float(portfolio_result['exp3'].iloc[-1])-10000)/10000,4))
        m2.metric(label="BAH", value=round((float(portfolio_result['bah'].iloc[-1])-10000)/10000,4))
        m3.metric(label="CRP", value=round((float(portfolio_result['crp'].iloc[-1])-10000)/10000,4))

        st.text("")

        st.markdown("### Daily Backtest Result")

        x = list(portfolio_result['dt'].values)
        #y = list(portfolio_value[graph_filter].values)[-100:]

        layout = plotly.graph_objs.Layout(xaxis={'type': 'category',
                                                 'dtick': 5})

        data = plotly.graph_objs.Line(x=x, y=portfolio_result[["exp3","bah","crp"]])

        fig = plotly.graph_objs.Figure([data], layout)

        fig.update_xaxes(tickangle= -45)  
        #fig = px.line(portfolio_value[-100:],x = 'x', y=graph_filter)
        st.plotly_chart(fig, use_container_width=True)

        
       






