import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Covid Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title(":chart_with_upwards_trend: Covid Dashboard")
st.markdown('<style> div.block-container{padding-top:1rem;}<style>', unsafe_allow_html=True)
st.markdown('<hr style="border:1px solid #48CBD8;">', unsafe_allow_html=True)

st.sidebar.subheader("Upload your csv file here")
# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    covid_data = pd.read_csv(uploaded_file)
    covid_data.rename(columns={'Date': 'date', 'Country/Region': 'country', 'Confirmed': 'cases', 'Deaths': 'deaths', 'Recovered': 'recovered'}, inplace=True)

    col1, col2 = st.columns(2)
    covid_data['date'] = pd.to_datetime(covid_data['date'])

    startDate = pd.to_datetime(covid_data['date']).min()
    endDate = pd.to_datetime(covid_data['date']).max()
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
    filtered_data_bar = covid_data[(covid_data['date'] >= date1) & (covid_data['date'] <= date2)].copy()

    st.sidebar.header("Choose your filter:")
    selected_region = st.sidebar.selectbox("Select WHO Region", covid_data['WHO Region'].unique())

    if selected_region:
        countries_in_region = covid_data[covid_data['WHO Region'] == selected_region]['country'].unique()

        if countries_in_region.size > 0:
            selected_country_pie = st.sidebar.selectbox("Select Country for Pie Chart", countries_in_region)
            selected_country_bar = st.sidebar.selectbox("Select Country for Bar Chart", countries_in_region)
        else:
            selected_country_pie = None
            selected_country_bar = None
    else:
        selected_country_pie = None
        selected_country_bar = None

    if selected_region and selected_country_pie:
        filtered_data_pie = covid_data[(covid_data['WHO Region'] == selected_region) & (covid_data['country'] == selected_country_pie) & (covid_data['date'] >= date1) & (covid_data['date'] <= date2)]
    else:
        
        filtered_data_pie = covid_data[(covid_data['date'] >= date1) & (covid_data['date'] <= date2)]

    if selected_region and selected_country_bar:
        filtered_data_bar = covid_data[(covid_data['WHO Region'] == selected_region) & (covid_data['country'] == selected_country_bar) & (covid_data['date'] >= date1) & (covid_data['date'] <= date2)]
    else:
      
        filtered_data_bar = covid_data[(covid_data['date'] >= date1) & (covid_data['date'] <= date2)]

    filtered_data = covid_data[(covid_data['date'] >= date1) & (covid_data['date'] <= date2)]
    st.subheader("Covid-19 Statistics")

    
    col1, padding, col2 = st.columns((12, 1, 12))

    with col1:
        total_cases_pie = filtered_data_pie['cases'].sum()
        total_deaths_pie = filtered_data_pie['deaths'].sum()
        total_recoveries_pie = filtered_data_pie['recovered'].sum()


        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div style="width: 23%; background-color: #e6f7ff; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #005580;">Cases</h3>
                    <p>{total_cases_pie}</p>
                </div>
                <div style="width: 23%; background-color: #ffb3b3; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #990000;">Deaths</h3>
                    <p>{total_deaths_pie}</p>
                </div>
                <div style="width: 38%; background-color: #ccffcc; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #008000;">Recoveries</h3>
                    <p>{total_recoveries_pie}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

     
        pie_chart = px.pie(
            filtered_data_pie.melt(id_vars=['date'], value_vars=['cases', 'deaths', 'recovered']),
            names='variable',
            values='value',
            color='variable',
            color_discrete_map={'cases': '#4dd2ff', 'deaths': '#ff8080', 'recovered': '#4dffb8'},
        )
        
        
        pie_chart.update_layout(height=500, width=500)

        st.plotly_chart(pie_chart)
        st.download_button(
            label="Download Pie Chart Data (CSV)",
            data=filtered_data_pie.melt(id_vars=['date'], value_vars=['cases', 'deaths', 'recovered']).to_csv(index=False, encoding='utf-8'),
            file_name='pie_chart_data.csv',
            key='download_pie_data',
            help="Download data for Pie Chart",
        )

      
    with col2:

        bar_chart_data = filtered_data_bar.melt(id_vars=['date'], value_vars=['cases', 'deaths', 'recovered'], var_name='Metric', value_name='Count')
        

        total_cases_bar = filtered_data_bar['cases'].sum()
        total_deaths_bar = filtered_data_bar['deaths'].sum()
      
        total_recoveries_bar = bar_chart_data[bar_chart_data['Metric'] == 'recovered']['Count'].sum()
    
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 80px;">
                <div style="width: 23%; background-color: #e6f7ff; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #005580;">Cases</h3>
                    <p>{total_cases_bar}</p>
                </div>
                <div style="width: 23%; background-color: #ffb3b3; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #990000;">Deaths</h3>
                    <p>{total_deaths_bar}</p>
                </div>
                <div style="width: 38%; background-color: #ccffcc; padding: 10px; border-radius: 8px; text-align: center;">
                    <h3 style="color: #008000;">Recoveries</h3>
                    <p>{total_recoveries_bar}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        bar_chart = px.bar(
            bar_chart_data,
            x='Metric',
            y='Count',
            title='Covid-19 Data',
            labels={'Count': 'Count', 'Metric': 'Metric'},
            color='Metric',
            color_discrete_map={'cases': '#4dd2ff', 'deaths': '#ff8080', 'recovered': '#4dffb8'},
        )

        bar_chart.update_layout(
            height=425,
            width=600,
            bargap=0.2,  
            title_text='Covid-19 Data',
        )


        bar_chart.update_yaxes(title_text='Count (in thousands)', tickformat=',')

        st.plotly_chart(bar_chart)
        bar_data_grouped = bar_chart_data.groupby(['Metric', 'date']).sum().reset_index()

       
        st.download_button(
            label="Download Bar Chart Data (CSV)",
            data=bar_data_grouped.to_csv(index=False, encoding='utf-8'),
            file_name='bar_chart_data.csv',
            key='download_bar_data',
            help="Download data for Bar Chart",
        )
    st.markdown('<hr style="border:1px solid #48CBD8;">', unsafe_allow_html=True)

    coll1, padding, coll2 = st.columns((12, 1, 12))

    with coll1:
        st.subheader("Deaths all over the world")

        fig_deaths = px.choropleth(
            filtered_data,
            locations='country',
            locationmode='country names',
            color='deaths',
            color_continuous_scale='Reds',
            labels={'deaths': 'Deaths'},
        )
        fig_deaths.update_layout(height=500, width=500)
        st.plotly_chart(fig_deaths)

    with coll2:
        st.subheader("Recoveries all over the world")
        fig_recoveries = px.choropleth(
            filtered_data,
            locations='country',
            locationmode='country names',
            color='recovered',
            color_continuous_scale='greens',
            labels={'recoveries': 'Recoveries'},
        )
        fig_recoveries.update_layout(height=500, width=500)
        st.plotly_chart(fig_recoveries)
    st.markdown('<hr style="border:1px solid #48CBD8;">', unsafe_allow_html=True)
    st.subheader("Cases all over the world")
    animated_choropleth_map = px.choropleth(
            filtered_data,
            locations='country',
            locationmode='country names',
            color='cases', 
            color_continuous_scale='Viridis',
            title='Animated Choropleth Map of COVID-19 Cases Over Time',
            animation_frame='date',
            labels={'cases': 'Cases'},
        )

    animated_choropleth_map.update_layout(height=650, width=900)
    st.plotly_chart(animated_choropleth_map)
   
    st.subheader("Percentage Contribution")

 
    total_cases = filtered_data['cases'].sum()
    total_deaths = filtered_data['deaths'].sum()
    total_recoveries = filtered_data['recovered'].sum()

   
    filtered_data['percentage_contribution'] = 0  
    st.markdown('<hr style="border:1px solid #48CBD8;">', unsafe_allow_html=True)


    if st.checkbox("Show Percentage Contribution"):
        percentage_contribution_type = st.selectbox("Select Percentage Contribution Type", ['Cases', 'Deaths', 'Recoveries'])

        if percentage_contribution_type == 'Cases':
            filtered_data['percentage_contribution'] = (filtered_data['cases'] / total_cases) * 100
        elif percentage_contribution_type == 'Deaths':
            filtered_data['percentage_contribution'] = (filtered_data['deaths'] / total_deaths) * 100
        elif percentage_contribution_type == 'Recoveries':
            filtered_data['percentage_contribution'] = (filtered_data['recovered'] / total_recoveries) * 100

      
        bar_chart = px.bar(
            filtered_data,
            x='country',
            y='percentage_contribution',
            title=f'Percentage Contribution of {percentage_contribution_type} by Country',
            labels={'percentage_contribution': 'Percentage Contribution'},
             color='percentage_contribution',  
            color_continuous_scale='Viridis',
        )

        bar_chart.update_layout(height=500, width=900)
        st.plotly_chart(bar_chart)
st.markdown('<hr style="border:1px solid #48CBD8;">', unsafe_allow_html=True)
