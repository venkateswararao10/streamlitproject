import streamlit as st
import pandas as pd
df=pd.read_csv('startupfundcleaned.csv')
df['date']=pd.to_datetime(df['date'])
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month
print(df.info())
st.set_page_config(layout='wide',page_title='StartUp Analysis')
st.sidebar.title('StartUp Analysis')
option=st.sidebar.selectbox('select any one',('Overall Analysis','Start Up','Investor'))
def load_overall_analysis():
    st.title('Overall Analysis')
    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby(['startup'])['amount'].max().sort_values(ascending=False).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
     # total funded startups
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('total',total)
    with col2:
        st.metric('Max', str(max_funding) + ' USD')
    with col3:
         st.metric('Avg',str(round(avg_funding)) + ' USD')
    with col4:
         st.metric('Funded Startups',num_startups)
    st.header('MOM investement')
    tab1, tab2= st.tabs(["total", "max"])
    with tab1:
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        st.line_chart(temp_df,x='x_axis',y='amount')
    with tab2:
        temp_df1= df.groupby(['year', 'month'])['amount'].max().reset_index()
        temp_df1['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        st.line_chart(temp_df1,x='x_axis',y='amount')
def loadinvestor(investor):
    st.title(investor)
    st.header('Recent Investments')
    st.dataframe(df[df['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']].head())
    st.header('Biggest investments')
    st.dataframe(df[df['investors'].str.contains(investor)].groupby(['startup'])['amount'].sum().head(1))
    tab1, tab2= st.tabs(["sector", "YoY investment graph"])
    with tab1:
        st.header("sector")
        st.line_chart(df[df['investors'].str.contains(investor)].groupby(['vertical'])['amount'].sum())
    with tab2:
        st.header("YoY investment graph")
        st.line_chart(df[df['investors'].str.contains(investor)].groupby(['year'])['amount'].sum())
def loadstartup(startup):
    st.title(startup)
if option=='Overall Analysis':
    load_overall_analysis()
elif option=='Start Up':
    st.title('Start Up Analysis')
    startup=st.sidebar.selectbox('Start Up',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Start Up Details')
    if btn1:
         loadstartup(startup)
elif option=='Investor':
    st.title('Investor Analysis')
    investor=st.sidebar.selectbox('Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn=st.sidebar.button('Find Investors Details')
    if btn:
        loadinvestor(investor)