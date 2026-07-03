import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Market Analytics Studio", layout="wide")
st.title("📈 Real-Time Financial Market Stock Tracker & Analytics Dashboard")
st.write("Stream live market telemetry data, calculate rolling technical indicators, and analyze global stock trends.")

st.write("---")

# 2. Sidebar Parameters Control Layout
st.sidebar.header("Market Controls")
ticker_symbol = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL, TSLA, NVDA, GOOG):", value="NVDA")
time_period = st.sidebar.selectbox("Select Historical Data Window:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
chart_type = st.sidebar.radio("Select Layout Type:", ["Candlestick Chart", "Line Trend Chart"])

# 3. Fetch Data Stream from Live API
with st.spinner(f"Connecting to live global market data nodes for {ticker_symbol.upper()}..."):
    try:
        stock_data = yf.Ticker(ticker_symbol)
        # Extract operational historical data frames
        df = stock_data.history(period=time_period)
        
        if df.empty:
            st.error(f"Ticker '{ticker_symbol.upper()}' could not be resolved. Please verify the market handle.")
        else:
            # 4. Feature Engineering: Compute Rolling Financial moving averages
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            
            # 5. Render Core Business Metrics
            info = stock_data.info
            company_name = info.get('longName', ticker_symbol.upper())
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                current_price = df['Close'].iloc[-1]
                st.metric(label="Current Closing Price", value=f"${current_price:,.2f}")
            with col2:
                day_high = df['High'].iloc[-1]
                st.metric(label="24h Session High", value=f"${day_high:,.2f}")
            with col3:
                day_low = df['Low'].iloc[-1]
                st.metric(label="24h Session Low", value=f"${day_low:,.2f}")
            with col4:
                volume = df['Volume'].iloc[-1]
                st.metric(label="Trading Volume", value=f"{volume:,}")
                
            st.write("---")
            st.subheader(f"📊 Quantitative Asset Valuation: {company_name}")
            
            # 6. Render Plotly Data Visualizations
            fig = go.Figure()
            
            if chart_type == "Candlestick Chart":
                fig.add_trace(go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    name="Market Execution"
                ))
            else:
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Base Line', line=dict(color='#00FFCC')))
                
            # Add Technical Indicators to the visual layout matrix
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], mode='lines', name='20-Day Moving Avg', line=dict(color='#FF9900', width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='50-Day Moving Avg', line=dict(color='#FF007F', width=1.5)))
            
            fig.update_layout(
                xaxis_rangeslider_visible=True,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=40, b=20),
                height=550
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 7. Render Raw Analytical Breakdown Matrix
            st.subheader("📋 Structured Transaction History Log")
            st.dataframe(df[['Open', 'High', 'Low', 'Close', 'Volume']].sort_index(ascending=False), use_container_width=True)
            
    except Exception as e:
        st.error(f"Telemetry Pipeline Error: {e}")