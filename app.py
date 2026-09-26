import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AUREX AI — Anshuman Dash",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #101d3a 0%, #070b14 35%, #05070c 100%);
    color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #070b14;
    border-right: 1px solid #1d2940;
}

[data-testid="stSidebar"] * {
    color: #e8edf5;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    background:
        linear-gradient(135deg, rgba(20,35,70,0.95), rgba(7,11,20,0.98));
    border: 1px solid #26385b;
    box-shadow: 0 0 40px rgba(0, 120, 255, 0.10);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #8fa7c9;
    font-size: 18px;
}

.creator {
    padding: 18px;
    border-radius: 18px;
    background: rgba(18, 29, 50, 0.8);
    border: 1px solid #26385b;
    margin-top: 20px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    background: rgba(13, 20, 34, 0.90);
    border: 1px solid #22314d;
    margin-bottom: 18px;
}

.metric-card {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, #101c31, #0a101c);
    border: 1px solid #26385b;
}

.section-title {
    font-size: 30px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 15px;
}

.small-text {
    color: #8fa7c9;
    font-size: 14px;
}

.warning {
    padding: 18px;
    border-radius: 15px;
    background: rgba(75, 53, 10, 0.35);
    border: 1px solid #70551b;
    color: #e8d18b;
}

.footer {
    text-align: center;
    color: #71809b;
    padding: 30px;
    border-top: 1px solid #1d2940;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# =========================================================
# DEMO MARKET DATA
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

def generate_prices(base_price=100, periods=180):
    np.random.seed(42)

    returns = np.random.normal(
        loc=0.0005,
        scale=0.018,
        size=periods
    )

    prices = [base_price]

    for r in returns:
        prices.append(prices[-1] * (1 + r))

    dates = pd.date_range(
        end=datetime.today(),
        periods=periods + 1
    )

    return pd.DataFrame({
        "Date": dates,
        "Price": prices
    })


def technical_analysis(df):

    data = df.copy()

    data["MA20"] = data["Price"].rolling(20).mean()
    data["MA50"] = data["Price"].rolling(50).mean()

    delta = data["Price"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

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


def investment_dna(price, change, sector):

    if change > 3:
        momentum = "High Momentum"
    elif change > 0:
        momentum = "Positive Momentum"
    else:
        momentum = "Weak Momentum"

    if sector == "Technology":
        style = "Growth / Innovation"
    elif sector == "Banking":
        style = "Financial / Value"
    elif sector == "Energy":
        style = "Cyclical / Commodity"
    else:
        style = "Mixed"

    return momentum, style


def create_chart(df, title):

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
        height=480,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Date",
        yaxis_title="Price"
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ◈ AUREX AI")

st.sidebar.markdown(
    "<div class='small-text'>Autonomous Universal Research & EXecution Intelligence</div>",
    unsafe_allow_html=True
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
    Anshuman Dash<br>
    <span class="small-text">AUREX AI</span>
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
            <div class="hero-title">◈ AUREX AI</div>
            <div class="hero-subtitle">
                Autonomous Universal Research & EXecution Intelligence
            </div>

            <div class="creator">
                Created & Developed by <b>Anshuman Dash</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>AI Investment Research Command Center</div>",
        unsafe_allow_html=True
    )

    st.write(
        """
        AUREX AI is a futuristic investment research platform designed
        to analyze markets, technical patterns, portfolio risk and
        strategy behavior in one interface.
        """
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Market Status",
        "ACTIVE"
    )

    col2.metric(
        "Assets Tracked",
        len(stocks)
    )

    col3.metric(
        "AI Modules",
        "8"
    )

    col4.metric(
        "Data Mode",
        "DEMO"
    )

    st.markdown("---")

    st.markdown("### 🚀 AUREX AI Capabilities")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="card">
            <h3>🧠 AI Research</h3>
            Analyze companies, sectors, trends and investment ideas.
            </div>

            <div class="card">
            <h3>📈 Technical Intelligence</h3>
            Study moving averages, RSI and price behavior.
            </div>

            <div class="card">
            <h3>💼 Portfolio Intelligence</h3>
            Understand portfolio allocation and basic risk exposure.
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="card">
            <h3>🧪 Strategy Laboratory</h3>
            Experiment with historical strategy simulations.
            </div>

            <div class="card">
            <h3>⚠️ Risk Observatory</h3>
            Explore volatility and potential risk factors.
            </div>

            <div class="card">
            <h3>🔬 Investment DNA</h3>
            Generate a simple profile of asset characteristics.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# AI RESEARCH LAB
# =========================================================

elif page == "🧠 AI Research Lab":

    st.markdown("## 🧠 AI Research Lab")

    st.write(
        "Use this prototype research engine to generate a structured investment research report."
    )

    company = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    research_type = st.selectbox(
        "Research Mode",
        [
            "Full Research",
            "Growth Analysis",
            "Risk Analysis",
            "Technical Analysis"
        ]
    )

    if st.button("🚀 Run AI Research"):

        data = stocks[company]

        st.session_state.analysis_history.append(
            f"{company} — {research_type}"
        )

        st.success("Research completed using demo data.")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Price",
            f"₹{data['price']}"
        )

        col2.metric(
            "Daily Change",
            f"{data['change']}%"
        )

        col3.metric(
            "Sector",
            data["sector"]
        )

        st.markdown("### Research Summary")

        if research_type == "Growth Analysis":

            st.write(
                f"""
                **Asset:** {company}

                **Sector:** {data['sector']}

                The demo dataset indicates a market asset that can be
                studied through price momentum, sector behavior,
                volume and longer-term trend analysis.
                """
            )

        elif research_type == "Risk Analysis":

            st.write(
                f"""
                **Asset:** {company}

                Risk should be evaluated using volatility,
                drawdowns, concentration, liquidity and market conditions.

                Current demo volume:
                **{data['volume']:,}**
                """
            )

        elif research_type == "Technical Analysis":

            df = generate_prices(data["price"])
            result = technical_analysis(df)

            (
                processed,
                latest,
                ma20,
                ma50,
                rsi,
                trend,
                momentum
            ) = result

            st.write(
                f"""
                **Trend:** {trend}

                **RSI:** {rsi:.2f}

                **Momentum:** {momentum}

                **20-day moving average:** ₹{ma20:.2f}

                **50-day moving average:** ₹{ma50:.2f}
                """
            )

            st.plotly_chart(
                create_chart(
                    processed,
                    f"{company} Technical Analysis"
                ),
                use_container_width=True
            )

        else:

            st.write(
                f"""
                AUREX AI Research Report for **{company}**

                Sector: **{data['sector']}**

                Current demo price: **₹{data['price']}**

                Daily movement: **{data['change']}%**

                Market capitalization: **{data['market_cap']}**

                The asset can be investigated using technical,
                fundamental, risk and portfolio analysis.
                """
            )

# =========================================================
# MARKET INTELLIGENCE
# =========================================================

elif page == "📊 Market Intelligence":

    st.markdown("## 📊 Market Intelligence")

    st.write(
        "Overview of the simulated assets currently tracked by AUREX AI."
    )

    market_df = pd.DataFrame(
        [
            {
                "Asset": name,
                "Price": data["price"],
                "Change %": data["change"],
                "Volume": data["volume"],
                "Sector": data["sector"],
                "Market Cap": data["market_cap"]
            }
            for name, data in stocks.items()
        ]
    )

    st.dataframe(
        market_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Market Overview")

    positive = sum(
        1 for data in stocks.values()
        if data["change"] > 0
    )

    negative = len(stocks) - positive

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Positive Assets",
        positive
    )

    c2.metric(
        "Negative Assets",
        negative
    )

    c3.metric(
        "Total Assets",
        len(stocks)
    )

# =========================================================
# TECHNICAL LABORATORY
# =========================================================

elif page == "📈 Technical Laboratory":

    st.markdown("## 📈 Technical Laboratory")

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        base_price=data["price"],
        periods=180
    )

    (
        processed,
        latest,
        ma20,
        ma50,
        rsi,
        trend,
        momentum
    ) = technical_analysis(df)

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
        create_chart(
            processed,
            f"{selected} — Technical Chart"
        ),
        use_container_width=True
    )

    st.markdown("### Technical Interpretation")

    st.write(
        f"""
        **Trend:** {trend}

        **Momentum:** {momentum}

        The moving-average relationship and RSI are simplified
        indicators used for educational research.
        """
    )

# =========================================================
# PORTFOLIO INTELLIGENCE
# =========================================================

elif page == "💼 Portfolio Intelligence":

    st.markdown("## 💼 Portfolio Intelligence")

    st.write(
        "Build a simple demo portfolio and examine its allocation."
    )

    portfolio = {}

    for stock in stocks:

        weight = st.slider(
            f"{stock} allocation (%)",
            min_value=0,
            max_value=100,
            value=25,
            step=5
        )

        portfolio[stock] = weight

    total = sum(portfolio.values())

    st.markdown("---")

    st.metric(
        "Total Allocation",
        f"{total}%"
    )

    if total == 100:

        st.success("Portfolio allocation is balanced to 100%.")

        portfolio_df = pd.DataFrame(
            {
                "Asset": list(portfolio.keys()),
                "Allocation": list(portfolio.values())
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
            "Adjust the allocations so the total equals 100%."
        )

# =========================================================
# STRATEGY LABORATORY
# =========================================================

elif page == "🧪 Strategy Laboratory":

    st.markdown("## 🧪 Strategy Laboratory")

    st.write(
        "Test a simple historical strategy using simulated data."
    )

    selected = st.selectbox(
        "Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        base_price=data["price"],
        periods=250
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
        height=480
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

    st.markdown("## ⚠️ Risk Observatory")

    selected = st.selectbox(
        "Select Asset",
        list(stocks.keys())
    )

    data = stocks[selected]

    df = generate_prices(
        base_price=data["price"],
        periods=250
    )

    daily_returns = df["Price"].pct_change().dropna()

    volatility = daily_returns.std() * np.sqrt(252) * 100

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

    st.markdown("### Risk Fact
