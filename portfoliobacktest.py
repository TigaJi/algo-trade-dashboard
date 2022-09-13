
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly


def portfolio_backtest_dashboard(drive):

    st.markdown("<h1 style='text-align: center;'>Strategy Backtest Results</h1>", unsafe_allow_html=True)

    #list of files
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    res_dict = {}
    res_list = []
    for file in file_list: 
        if "_backtest_result.csv" in file['title']:
            title = file['title'][:-20]
            res_list.append(title)
            res_dict[title] = file['id']
    
    strategy = st.selectbox("Select Strategy",res_list)

    placeholder = st.empty()
    with placeholder.container():
        f = drive.CreateFile({'id': res_dict[strategy]})
        f.GetContentFile(strategy)

        df = pd.read_csv(strategy)

        x = df['dt']
        values = df['total_value']
        bah = df['bah']

        layout = plotly.graph_objs.Layout(xaxis={'type': 'category',
                                                 'dtick': len(x)/20})

        fig = plotly.graph_objects.Figure(layout = layout)

        fig.add_trace(plotly.graph_objects.Scatter(x=x, y=values,
                    mode='lines',
                    name=strategy))

        fig.add_trace(plotly.graph_objects.Scatter(x=x, y=bah,
                    mode='lines',
                    name='Buy and hold'))
        
        fig.update_xaxes(tickangle= -45)  

        st.plotly_chart(fig, use_container_width=True)


            


    
    '''
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

        
       





'''
