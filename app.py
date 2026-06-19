import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide"
)

st.title("📈 Real-Time Stock Market Dashboard")

ticker = st.text_input(
    "Enter Stock Symbol",
    "AAPL"
)

if ticker:

    stock = yf.Ticker(ticker)

    data = stock.history(period="6mo")

    if not data.empty:

        latest_price = data["Close"].iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"${latest_price:.2f}"
        )

        col2.metric(
            "Highest Price",
            f"${data['High'].max():.2f}"
        )

        col3.metric(
            "Lowest Price",
            f"${data['Low'].min():.2f}"
        )

        data["MA20"] = (
            data["Close"]
            .rolling(20)
            .mean()
        )

        fig = px.line(
            data,
            x=data.index,
            y=["Close", "MA20"],
            title=f"{ticker} Stock Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Stock Data")

        st.dataframe(data.tail(20))

    else:
        st.error("Invalid Stock Symbol")