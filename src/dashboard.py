import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from config import DB_CONFIG

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

# Streamlit App
def main():
    st.title("UNData Dashboard")
    st.sidebar.title("Navigation")

    # Sidebar navigation
    options = ["Animals", "Meats", "Fishes"]
    choice = st.sidebar.selectbox("Select a table", options)

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
            
            # Display total records
            st.write(f"Total records: {len(df)}")
            
            # Add a year filter
            years = sorted(df["Year"].unique())
            selected_year = st.selectbox("Filter by Year", ["All"] + list(years))
            
            if selected_year != "All":
                df = df[df["Year"] == selected_year]
            
            # Display filtered data
            st.dataframe(df)
            
            # Add visualizations
            st.subheader("Visualizations")
            
            # Bar chart: Trade (USD) by Country
            st.write("### Trade (USD) by Country")
            trade_by_country = df.groupby("Country or Area")["Trade (USD)"].sum().reset_index()
            fig = px.bar(trade_by_country, x="Country or Area", y="Trade (USD)", title="Trade (USD) by Country")
            st.plotly_chart(fig)
            
            # Pie chart: Trade (USD) by Flow
            st.write("### Trade (USD) by Flow")
            trade_by_flow = df.groupby("Flow")["Trade (USD)"].sum().reset_index()
            fig = px.pie(trade_by_flow, values="Trade (USD)", names="Flow", title="Trade (USD) by Flow")
            st.plotly_chart(fig)
            
            # Line chart: Trade (USD) Over Time
            st.write("### Trade (USD) Over Time")
            trade_over_time = df.groupby("Year")["Trade (USD)"].sum().reset_index()
            fig = px.line(trade_over_time, x="Year", y="Trade (USD)", title="Trade (USD) Over Time")
            st.plotly_chart(fig)
        else:
            st.warning("No data found.")

# Run the Streamlit app
if __name__ == "__main__":
    main()