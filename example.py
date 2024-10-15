import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import datetime as dt


def stock_name(name):
    name = name.upper()
    name = name.replace(" ", "")
    n = name + '.NS'
    return n


st.title("Interactive Stock Price Viewer")

name = st.text_input("Enter the name of the company:")

start_date = st.date_input("Start Date", dt.date(2020, 1, 1))
end_date = st.date_input("End Date", dt.date.today())

if start_date > end_date:
    st.error("Error: End date must be after the start date.")

if st.button('Get Stock Data') and name:
    n = stock_name(name)

    try:
        data = yf.download(n, start=start_date, end=end_date)

        # Invert the DataFrame
        data = data.iloc[::-1]

        st.write(f"Stock Data for {name} from {start_date} to {end_date}:")
        st.dataframe(data)

        st.write("Interactive Closing Price Chart:")
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='blue')))

        fig.update_layout(
            title=f"{name} Stock Closing Prices",
            xaxis_title="Date",
            yaxis_title="Closing Price (INR)",
            hovermode="x unified",
            template="plotly_dark"
        )

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error fetching data for {name}: {e}")
