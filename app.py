import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AUREX AI - Anshuman Dash",
    page_icon="◈",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #070b14;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #090d17;
    }

    .hero {
        padding: 35px;
        border-radius: 20px;
        background-color: #101a2e;
        border: 1px solid #263b60;
        margin-bottom: 25px;
    }

    .card {
        padding: 20px;
        border-radius: 16px;
        background-color: #0f1726;
        border: 1px solid #243653;
        margin-bottom: 15px;
    }

    .creator {
        padding: 15px;
        border-radius: 12px;
        background-color: #111d31;
        border: 1px solid #294064;
    }

    .footer {
        text-align: center;
        padding: 30px;
        color: #71809b;
        margin-top: 40px;
        border-top: 1px solid #1d2940;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DEMO DATA
# =========================================================

stocks = {
    "AUREX DEMO": {
        "price": 248.60,
        "change": 3.42,
        "volume": 1245000,
        "sector": "Technology",
        "market_cap": "₹2.8T"
    },
    "NEXUS TECH": {
        "price": 186.40,
        "change": 1.85,
        "volume": 982000,
        "sector": "Technology",
        "market_cap": "₹1.9T"
    },
    "ORBIT BANK": {
        "price": 94.75,
        "change": -0.72,
        "volume": 2100000,
        "sector": "Banking",
        "market_cap": "₹1.4T"
    },
    "ZENITH ENERGY": {
        "price": 312.20,
        "change": 4.12,
        "volume": 765000,
        "sector": "Energy",
        "market_cap": "₹3.1T"
    }
}

# =========================================================
# FUNCTIONS
# =========================================================

def generate_prices(base_price, periods=180):

    np.random.seed(42)

    returns = np.random.normal(
        0.0005,
        0.018,
        periods
    )

    prices = [base_price]

    for value in returns:
        new_price = prices[-1] * (1 + value)
        prices.append(new_price)

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=periods + 1
    )

    return pd.DataFrame({
        "Date": dates,
        "Price": prices
    })


def calculate_indicators(df):

    data = df.copy()

    data["MA20"] = data["Price"].rolling(20).mean()
    data["MA50"] = data["Price"].rolling(50).mean()

    difference = data["Price"].diff()

    gain = difference.clip(lower=0)
    loss = -difference.clip(upper=0)

    average_gain = gain.rolling(14).mean()
    average_loss = loss.rolling(14).mean()

    rs = average_gain / average_loss.replace(0, np.nan)

    data["RSI"] = 100 - (100 / (1 + rs))

    latest_price = data["Price"].iloc[-1]
    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]
    rsi = data["RSI"].iloc[-1]

    if ma20 > ma50:
        trend = "Bullish"
    else:
        trend = "Bearish"

    if rsi >= 70:
        momentum = "Overbought"
    elif rsi <= 30:
        momentum = "Oversold"
    else:
        momentum = "Neutral"

    return data, latest_price, ma20, ma50, rsi, trend, momentum


def price_chart(df, title):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Price"],
            mode="lines",
            name="Price"
        )
    )

    if "MA20" in df.columns:

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["MA20"],
                mode="lines",
                name="MA20"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["MA50"],
                mode="lines",
                name="MA50"
            )
        )

    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=450
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("◈ AUREX AI")

st.sidebar.caption(
    "Autonomous Universal Research & EXecution Intelligence"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "◈ Command Center",
        "🧠 AI Research Lab",
        "📊 Market Intelligence",
        "📈 Technical Laboratory",
        "💼 Portfolio Intelligence",
        "🧪 Strategy Laboratory",
        "⚠️ Risk Observatory",
        "🔬 Investment DNA"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div class="creator">
    <b>Creator & Developer</b><br><br>
    Anshuman Dash
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# COMMAND CENTER
# =========================================================

if page == "◈ Command Center":

    st.markdown(
        """
        <div class="hero">
        <h1>◈ AUREX AI</h1>
        <h3>Autonomous Universal Research & EXecution Intelligence</h3>
        <br>
        Created & Developed by <b>Anshuman Dash</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("AI Investment Research Command Center")

    st.write(
        "AUREX AI is a futuristic investment research platform "
        "for studying markets, technical patterns, portfolio risk "
        "and trading strategies."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Market Status", "ACTIVE")
    col2.metric("Assets Tracked", len(stocks))
    col3.metric("AI Modules", "8")
    col4.metric("Data Mode", "DEMO")

    st.markdown("---")

    st.subheader("AUREX AI Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">
            <h3>🧠 AI Research</h3>
            Research companies, sectors and market ideas.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">
            <h3>📈 Technical Intelligence</h3>
            Analyze price trends, moving averages and RSI.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">
            <h3>💼 Portfolio Intelligence</h3>
            Study portfolio allocation.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">
            <h3>🧪 Strategy Laboratory</h3>
            Test simple historical strategies.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">
            <h3>⚠️ Risk Observatory</h3>
            Examine volatility and drawdown.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">
            <h3>🔬 Investment DNA</h3>
            Generate an asset profile.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# AI RESEARCH LAB
# =========================================================

elif page == "🧠 AI Research Lab":

    st.header("🧠 AI Research Lab")

    st.write(
        "Generate a simple research report using the demo market data."
    )

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    mode = st.selectbox(
        "Research Mode",
        [
            "Full Research",
            "Growth Analysis",
            "Risk Analysis",
            "Technical Analysis"
        ]
    )

    if st.button("🚀 Run AI Research"):

        data = stocks[selected]

        st.success("Research completed.")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Price",
            f"₹{data['price']:.2f}"
        )

        col2.metric(
            "Daily Change",
            f"{data['change']:.2f}%"
        )

        col3.metric(
            "Sector",
            data["sector"]
        )

        st.subheader("Research Report")

        if mode == "Full Research":

            st.write(
                f"Asset: {selected}"
            )

            st.write(
                f"Sector: {data['sector']}"
            )

            st.write(
                f"Market Capitalization: {data['market_cap']}"
            )

            st.write(
                f"Trading Volume: {data['volume']:,}"
            )

            st.write(
                "The asset can be studied using price behavior, "
                "technical indicators, volume, risk and portfolio analysis."
            )

        elif mode == "Growth Analysis":

            st.write(
                f"{selected} belongs to the {data['sector']} sector."
            )

            st.write(
                "Growth research should consider revenue growth, "
                "earnings, valuation, competition and industry trends."
            )

        elif mode == "Risk Analysis":

            st.write(
                f"Current demo trading volume: {data['volume']:,}"
            )

            st.write(
                "Risk analysis should consider volatility, drawdowns, "
                "liquidity, concentration and market conditions."
            )

        else:

            df = generate_prices(
                data["price"]
            )

            (
                processed,
                latest,
                ma20,
                ma50,
                rsi,
                trend,
                momentum
            ) = calculate_indicators(df)

            st.write(
                f"Trend: {trend}"
            )

            st.write(
                f"RSI: {rsi:.2f}"
            )

            st.write(
                f"Momentum: {momentum}"
            )

            st.plotly_chart(
                price_chart(
                    processed,
                    f"{selected} Technical Analysis"
                ),
                use_container_width=True
            )

# =========================================================
# MARKET INTELLIGENCE
# =========================================================

elif page == "📊 Market Intelligence":

    st.header("📊 Market Intelligence")

    rows = []

    for name, data in stocks.items():

        rows.append(
            {
                "Asset": name,
                "Price": data["price"],
                "Change %": data["change"],
                "Volume": data["volume"],
                "Sector": data["sector"],
                "Market Cap": data["market_cap"]
            }
        )

    market_df = pd.DataFrame(rows)

    st.dataframe(
        market_df,
        use_container_width=True,
        hide_index=True
    )

    positive = sum(
        data["change"] > 0
        for data in stocks.values()
    )

    negative = len(stocks) - positive

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Positive Assets",
        positive
    )

    col2.metric(
        "Negative Assets",
        negative
    )

    col3.metric(
        "Total Assets",
        len(stocks)
    )

# =========================================================
# TECHNICAL LABORATORY
# =========================================================

elif page == "📈 Technical Laboratory":

    st.header("📈 Technical Laboratory")

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        data["price"],
        180
    )

    (
        processed,
        latest,
        ma20,
        ma50,
        rsi,
        trend,
        momentum
    ) = calculate_indicators(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Price",
        f"₹{latest:.2f}"
    )

    col2.metric(
        "MA20",
        f"₹{ma20:.2f}"
    )

    col3.metric(
        "MA50",
        f"₹{ma50:.2f}"
    )

    col4.metric(
        "RSI",
        f"{rsi:.2f}"
    )

    st.plotly_chart(
        price_chart(
            processed,
            f"{selected} Price Chart"
        ),
        use_container_width=True
    )

    st.subheader("Technical Interpretation")

    st.write(
        f"Trend: {trend}"
    )

    st.write(
        f"Momentum: {momentum}"
    )

    st.write(
        "These indicators are simplified research tools and should "
        "not be treated as guaranteed trading signals."
    )

# =========================================================
# PORTFOLIO INTELLIGENCE
# =========================================================

elif page == "💼 Portfolio Intelligence":

    st.header("💼 Portfolio Intelligence")

    st.write(
        "Create a simple demo portfolio."
    )

    allocation = {}

    for name in stocks:

        allocation[name] = st.slider(
            name + " allocation (%)",
            0,
            100,
            25,
            5
        )

    total = sum(allocation.values())

    st.metric(
        "Total Allocation",
        f"{total}%"
    )

    if total == 100:

        st.success(
            "Portfolio allocation equals 100%."
        )

        portfolio_df = pd.DataFrame(
            {
                "Asset": list(allocation.keys()),
                "Allocation": list(allocation.values())
            }
        )

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=portfolio_df["Asset"],
                    values=portfolio_df["Allocation"],
                    hole=0.45
                )
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Make the total allocation exactly 100%."
        )

# =========================================================
# STRATEGY LABORATORY
# =========================================================

elif page == "🧪 Strategy Laboratory":

    st.header("🧪 Strategy Laboratory")

    st.write(
        "Test a simple moving-average strategy using simulated historical data."
    )

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        data["price"],
        250
    )

    df["MA20"] = df["Price"].rolling(20).mean()
    df["MA50"] = df["Price"].rolling(50).mean()

    df["Signal"] = np.where(
        df["MA20"] > df["MA50"],
        1,
        0
    )

    df["Market Return"] = df["Price"].pct_change()

    df["Strategy Return"] = (
        df["Signal"].shift(1) *
        df["Market Return"]
    )

    df["Strategy Equity"] = (
        1 + df["Strategy Return"].fillna(0)
    ).cumprod()

    df["Buy Hold Equity"] = (
        1 + df["Market Return"].fillna(0)
    ).cumprod()

    strategy_return = (
        df["Strategy Equity"].iloc[-1] - 1
    ) * 100

    buy_hold_return = (
        df["Buy Hold Equity"].iloc[-1] - 1
    ) * 100

    col1, col2 = st.columns(2)

    col1.metric(
        "Strategy Return",
        f"{strategy_return:.2f}%"
    )

    col2.metric(
        "Buy & Hold Return",
        f"{buy_hold_return:.2f}%"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Strategy Equity"],
            mode="lines",
            name="Strategy"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Buy Hold Equity"],
            mode="lines",
            name="Buy & Hold"
        )
    )

    fig.update_layout(
        title="Strategy Simulation",
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning(
        "This is a simulated historical experiment. "
        "It is not a prediction or guarantee of future returns."
    )

# =========================================================
# RISK OBSERVATORY
# =========================================================

elif page == "⚠️ Risk Observatory":

    st.header("⚠️ Risk Observatory")

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        data["price"],
        250
    )

    daily_returns = df["Price"].pct_change().dropna()

    volatility = (
        daily_returns.std() *
        np.sqrt(252) *
        100
    )

    running_max = df["Price"].cummax()

    drawdown = (
        (df["Price"] - running_max) /
        running_max
    ) * 100

    maximum_drawdown = drawdown.min()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Annualized Volatility",
        f"{volatility:.2f}%"
    )

    col2.metric(
        "Maximum Drawdown",
        f"{maximum_drawdown:.2f}%"
    )

    col3.metric(
        "Trading Volume",
        f"{data['volume']:,}"
    )

    st.subheader("Risk Factors")

    st.write(
        "• Price volatility"
    )

    st.write(
        "• Maximum drawdown"
    )

    st.write(
        "• Liquidity"
    )

    st.write(
        "• Sector concentration"
    )

    st.write(
        "• Market conditions"
    )

    st.write(
        "• Strategy dependence"
    )

    st.write(
        "• Limitations of historical data"
    )

# =========================================================
# INVESTMENT DNA
# =========================================================

elif page == "🔬 Investment DNA":

    st.header("🔬 Investment DNA")

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    if data["change"] > 3:
        momentum = "High Momentum"
    elif data["change"] > 0:
        momentum = "Positive Momentum"
    else:
        momentum = "Weak Momentum"

    if data["sector"] == "Technology":
        style = "Growth / Innovation"
    elif data["sector"] == "Banking":
        style = "Financial / Value"
    elif data["sector"] == "Energy":
        style = "Cyclical / Commodity"
    else:
        style = "Mixed"

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Momentum",
        momentum
    )

    col2.metric(
        "Sector",
        data["sector"]
    )

    col3.metric(
        "Style",
        style
    )

    st.subheader("Asset Profile")

    st.write(
        f"Asset: {selected}"
    )

    st.write(
        f"Price: ₹{data['price']:.2f}"
    )

    st.write(
        f"Daily Change: {data['change']:.2f}%"
    )

    st.write(
        f"Sector: {data['sector']}"
    )

    st.write(
        f"Market Cap: {data['market_cap']}"
    )

    st.write(
        f"Volume: {data['volume']:,}"
    )

    st.write(
        f"Momentum Profile: {momentum}"
    )

    st.write(
        f"Investment Style: {style}"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    <b>◈ AUREX AI</b><br><br>
    Autonomous Universal Research & EXecution Intelligence<br><br>
    Created & Developed by <b>Anshuman Dash</b><br><br>
    Prototype investment research platform • Demo data • Not financial advice
    </div>
    """,
    unsafe_allow_html=True
)
