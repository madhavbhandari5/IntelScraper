# dashboard.py
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from config import DB_CONFIG

# Set page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="UNData Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stDataFrame {
            width: 100%;
        }
        .metric {
            text-align: center;
        }
        .stSelectbox, .stMultiSelect, .stSlider {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Function to connect to the MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to fetch data from a table
def fetch_data(table_name):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            return data
        except Exception as e:
            st.error(f"Error fetching data from {table_name}: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    else:
        return []

# Function to clean and convert numeric columns
def clean_data(df):
    # Convert numeric columns
    numeric_cols = ['Trade (USD)', 'Weight (kg)', 'Quantity']
    for col in numeric_cols:
        if col in df.columns:
            # Remove commas and convert to float
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# Streamlit App
def main():
    st.title("🌍 UNData Dashboard")
    st.sidebar.title("Navigation")

    # Sidebar navigation
    options = ["Animals", "Meats", "Fishes", "Dairies", "AnimalOriginated", "Trees"]
    choice = st.sidebar.selectbox("Select a table", options)

    # About section in sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        """
        **UNData Dashboard**  
        Visualizing UN ComTrade data for various commodity categories.  
        Data source: [UN ComTrade Database](https://comtrade.un.org/)
        """
    )

    # Fetch and display data based on user choice
    if choice:
        st.header(f"{choice} Data")
        data = fetch_data(choice)
        
        if data:
            # Convert data to a DataFrame
            df = pd.DataFrame(data, columns=[
                "ID", "Country or Area", "Year", "Commodity", "Flow", 
                "Trade (USD)", "Weight (kg)", "Quantity Name", "Quantity"
            ])
            
            # Clean and convert numeric columns
            df = clean_data(df)
            
            # Display total records
            st.write(f"Total records: {len(df)}")
            
            # Add filters in the sidebar
            st.sidebar.header("Filters")
            
            # Year filter
            years = sorted(df["Year"].unique())
            selected_year = st.sidebar.selectbox(
                "Filter by Year", 
                ["All"] + list(years),
                index=0
            )
            
            # Multi-select for countries
            countries = sorted(df["Country or Area"].unique())
            selected_countries = st.sidebar.multiselect(
                "Select Countries", 
                countries, 
                default=countries[:3] if len(countries) > 3 else countries
            )
            
            # Flow type filter
            flows = sorted(df["Flow"].unique())
            selected_flows = st.sidebar.multiselect(
                "Select Flow Types", 
                flows, 
                default=flows
            )
            
            # Apply filters
            if selected_year != "All":
                df = df[df["Year"] == selected_year]
            if selected_countries:
                df = df[df["Country or Area"].isin(selected_countries)]
            if selected_flows:
                df = df[df["Flow"].isin(selected_flows)]
            
            # Display key metrics
            st.subheader("Key Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trade (USD)", f"${df['Trade (USD)'].sum():,.2f}")
            col2.metric("Total Weight (kg)", f"{df['Weight (kg)'].sum():,.2f} kg")
            col3.metric("Unique Countries", len(df['Country or Area'].unique()))
            
            # Display filtered data with expander
            with st.expander("View Filtered Data"):
                st.dataframe(df)
            
            # Summary statistics
            with st.expander("View Summary Statistics"):
                st.write(df.describe())
            
            # Visualizations
            st.subheader("Visualizations")
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Trade Overview", 
                "Geographical", 
                "Time Series", 
                "Commodity Analysis", 
                "Correlations"
            ])
            
            with tab1:
                # Bar chart: Trade (USD) by Country
                st.write("### Trade (USD) by Country")
                trade_by_country = df.groupby("Country or Area")["Trade (USD)"].sum().reset_index()
                fig = px.bar(
                    trade_by_country, 
                    x="Country or Area", 
                    y="Trade (USD)", 
                    title="Trade (USD) by Country",
                    color="Trade (USD)",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Pie chart: Trade (USD) by Flow
                st.write("### Trade (USD) by Flow")
                trade_by_flow = df.groupby("Flow")["Trade (USD)"].sum().reset_index()
                fig = px.pie(
                    trade_by_flow, 
                    values="Trade (USD)", 
                    names="Flow", 
                    title="Trade (USD) by Flow",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Geographical visualization
                try:
                    import pycountry
                    
                    st.write("### Geographical Distribution")
                    
                    # Attempt to convert country names to ISO codes
                    def get_country_code(name):
                        try:
                            return pycountry.countries.search_fuzzy(name)[0].alpha_3
                        except:
                            return None
                    
                    geo_df = df.copy()
                    geo_df['country_code'] = geo_df['Country or Area'].apply(get_country_code)
                    geo_df = geo_df.dropna(subset=['country_code'])
                    
                    if not geo_df.empty:
                        fig = px.choropleth(
                            geo_df.groupby('country_code')['Trade (USD)'].sum().reset_index(),
                            locations="country_code",
                            color="Trade (USD)",
                            hover_name="country_code",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title="Trade Value by Country"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Could not map country names to codes for geographical visualization.")
                except ImportError:
                    st.warning("Install pycountry (`pip install pycountry`) for geographical visualizations.")
            
            with tab3:
                # Time series analysis
                st.write("### Time Series Analysis")
                
                if selected_year == "All":  # Only show if not filtered by year
                    ts_col = st.selectbox(
                        "Select metric for time series", 
                        ["Trade (USD)", "Weight (kg)", "Quantity"]
                    )
                    
                    fig = px.line(
                        df.groupby(['Year', 'Flow'])[ts_col].sum().reset_index(),
                        x='Year',
                        y=ts_col,
                        color='Flow',
                        title=f"{ts_col} Over Time by Flow",
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Time series analysis is available when 'All' years are selected.")
            
            with tab4:
                # Commodity analysis
                st.write("### Commodity Analysis")
                top_n = st.slider("Show top N commodities", 5, 20, 10)
                
                # Ensure we're working with numeric data
                if pd.api.types.is_numeric_dtype(df['Trade (USD)']):
                    top_commodities = df.groupby('Commodity')['Trade (USD)'].sum().nlargest(top_n).index
                    
                    fig = px.bar(
                        df[df['Commodity'].isin(top_commodities)].groupby('Commodity')['Trade (USD)'].sum().reset_index(),
                        x='Commodity',
                        y='Trade (USD)',
                        title=f"Top {top_n} Commodities by Trade Value",
                        color="Trade (USD)",
                        color_continuous_scale="Bluered"
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Trade data is not in numeric format. Cannot display commodity analysis.")
            
            with tab5:
                # Correlation analysis
                st.write("### Correlation Analysis")
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols].corr()
                    
                    fig = px.imshow(
                        corr_matrix,
                        text_auto=True,
                        aspect="auto",
                        title="Correlation Matrix",
                        color_continuous_scale="RdBu",
                        zmin=-1,
                        zmax=1
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Not enough numeric columns for correlation analysis.")
            
            # Data export options
            st.sidebar.header("Data Export")
            if st.sidebar.button("Download Current View as CSV"):
                csv = df.to_csv(index=False)
                st.sidebar.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{choice.lower()}_data.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No data found.")

# Run the Streamlit app
if __name__ == "__main__":
    main()