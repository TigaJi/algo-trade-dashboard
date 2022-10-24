
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

        ret = (df['total_value'].values[-1]-df['total_value'].values[0])/df['total_value'].values[0]
        bah_ret = (df['bah'].values[-1]-df['bah'].values[0])/df['bah'].values[0]
        m1,m2 = st.columns(2)
        
        m1.metric(label="return", value = round(ret,4))
        m2.metric(label='bah return', value = round(bah_ret,4))


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


            
