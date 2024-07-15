import streamlit as st
import duckdb as db
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from streamlit_option_menu import option_menu
  
def analysis():

    #getting the data
    uploaded_file = "./Noon.csv"

    st.subheader('Data Statistics')
    noon = pd.read_csv(uploaded_file)

    #some data cleaning
    noon.loc[noon['brand_en'] == 'JAYJUN JJ', 'brand_en'] = 'JAYJUN'    

    #data to be shown in big
    query = db.sql("select count(distinct brand_en) as 'brand', marketplace,  id_partner, sum (invoice_price) as 'sales' from noon group by marketplace, id_partner").df()
    #st.dataframe(query, column_order=['brand','Total Sales'])
    col1, col2 = st.columns(2)
    col1.metric("Total Brands", query["brand"])
    col2.metric("Total Sales", query["sales"])


    with st.expander("Data Preview"):
        st.dataframe(noon,column_order=['sku','brand_en','title_en','invoice_price','ordered_date','delivered_date','cancelled_date','returned_date'])
    
#    tab1, tab2, tab3, tab4= st.tabs(["Product Analysis", "Brand Analysis", "Orders", "Inventory"])
    tab1, tab2 = st.tabs(["Product Analysis", "Brand Analysis"])

    with tab1:
        #Product Analysis
        n_product_analysis()
        
    with tab2:
        n_brand_analysis()

'''    with tab3:
        st.title('Orders')
        st.text('aedtbtbhhsrtgbhsthbsrth')
        st.divider()
        
    with tab4:
        st.title('Inventory')
        st.text('sfgnsnsrgnsrgngtr')
        st.divider()    '''

def orders():
    st.subheader("Noon Orders")
    st.divider()

def inventory():
    st.subheader("Noon Inventory")
    st.divider()

def n_product_analysis():
    st.subheader("Product Analysis" )
    query2 = db.sql("select sku, title_en, count(title_en),sum(invoice_price)from noon group by title_en, sku order by sum(invoice_price) desc").df()
    st.dataframe(query2, use_container_width=True)
    st.divider()
    #day-wise Analysis
    query3 = db.sql("select ordered_date as day, sum(invoice_price) from noon group by ordered_date order by ordered_date desc").df()

    #Top 10 products
    query4 = db.sql("select sku, title_en, brand_en, count(title_en) as sold, sum(invoice_price) from noon group by title_en, sku, brand_en order by sold desc limit 10").df()
    #st.dataframe(query4)

    #st.

    #showing the horizontal bar chart for top 10 products using plotly 

    x1 = np.array(query4['sku'] )
    y1 =np.array(query4['sold'])

    print(x1)
    print(y1)

    fig = make_subplots()

    # Creating a bar chart
    fig = go.Figure(go.Bar(
        x=y1,
        y=x1,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Top 10 Products',
        orientation='h',
        textposition='auto',
        text = y1
    ))

    # Updating layout of the chart
    fig.update_layout(
        title='Top 10 Products by Sales',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        
    )

    # Displaying the figure using Streamlit
    #st.

    col1, col2 = st.columns([3,1],gap='large', vertical_alignment="bottom")

    col1.subheader("Top 10 Products")
    col1.plotly_chart(fig)

    col2.subheader("Day-wise Sales")
    col2.dataframe(query3)
    st.divider()

def n_brand_analysis():
    #noon orders data along with sales - brandwise
    query1 = db.sql("SELECT brand_en as brand, sum(invoice_price) as sales, count(ordered_date) as orders, count(cancelled_date) as cancelled, count(returned_date) as returned, count(delivered_date) as total_delivery from noon group by brand_en").df()
    query1x = db.sql("select count(cancelled_date) as cancelled, count(returned_date) as returned, count(delivered_date) as total_delivery from noon").df()

    pie1 = px.pie(query1, values='sales', names='brand',hover_data='orders', labels={'brand':'Brand ','sales':'Total Sales ','orders':'Total Orders '}, color_discrete_sequence=px.colors.sequential.RdBu_r)

    col1, col2 = st.columns([0.8, 0.7],gap='small')

    col1.subheader("Brand Analysis")
    col1.dataframe(query1)

    col2.subheader("Sales by Brands")
    col2.plotly_chart(pie1)
    st.divider()


def noon_page():
    select = option_menu(None,
                         ["Analysis", "Orders", "Inventory"], 
                         icons=['house','house','house'],
                         default_index=0, 
                         orientation="horizontal")
    tab_to_funcs = {
        "Analysis" : analysis,
        "Orders": orders,
        "Inventory" : inventory,    
    }
    tab_to_funcs[select]()