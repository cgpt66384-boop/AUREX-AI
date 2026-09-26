import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# AUREX AI — API-KEY-FREE INVESTMENT RESEARCH LAB
# =========================================================

st.set_page_config(
    page_title="AUREX AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CSS
# -------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(40,120,255,0.12), transparent 25%),
        radial-gradient(circle at 85% 20%, rgba(140,60,255,0.10), transparent 25%),
        #05070d;
    color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background: #080b13;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #dce3ef !important;
}

.aurex-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 0;
}

.aurex-subtitle {
    color: #8995aa;
    font-size: 14px;
    margin-top: -5px;
}

.hero {
    padding: 30px;
    border-radius: 24px;
    background:
        linear-gradient(135deg,
        rgba(21,29,52,0.95),
        rgba(8,11,20,0.95));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 70px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    margin-bottom: 5px;
}

.hero p {
    color: #8e9ab0;
}

.metric-card {
    background: rgba(17,22,36,0.90);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 20px;
    min-height: 120px;
}

.metric-title {
    color: #8995aa;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-small {
    color: #7f8ba0;
    font-size: 12px;
}

.section-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 15px;
}

.research-box {
    background: rgba(13,18,30,0.95);
    border: 1px solid rgba(70,130,255,0.20);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 50px;
    background: rgba(70,130,255,0.12);
    border: 1px solid rgba(70,130,255,0.25);
    color: #9bbcff;
    font-size: 12px;
}

.disclaimer {
    background: rgba(255,180,0,0.06);
    border: 1px solid rgba(255,180,0,0.18);
    border-radius: 14px;
    padding: 15px;
    color: #b9a878;
    font-size: 12px;
}

div[data-testid="stMetric"] {
    background: rgba(17,22,36,0.9);
    border-radius: 16px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DEMO DATA ENGINE
# =========================================================

np.random.seed(42)

stocks = {
    "AUREX DEMO": {
        "price": 2480.50,
        "sector": "Technology",
        "market_cap": "₹12.4T",
        "pe": 28.4,
        "roe": 22.8,
        "revenue_growth": 17.5,
        "debt": 0.24,
    },
    "NEXUS TECH": {
        "price": 1845.20,
        "sector": "Technology",
        "market_cap": "₹8.7T",
        "pe": 34.8,
        "roe": 25.2,
        "revenue_growth": 24.1,
        "debt": 0.18,
    },
    "ORBIT BANK": {
        "price": 1260.80,
        "sector": "Financials",
        "market_cap": "₹6.2T",
        "pe": 18.7,
        "roe": 17.9,
        "revenue_growth": 13.2,
        "debt": 0.42,
    },
    "ZENITH ENERGY": {
        "price": 912.40,
        "sector": "Energy",
        "market_cap": "₹5.4T",
        "pe": 21.5,
        "roe": 19.4,
        "revenue_growth": 11.8,
        "debt": 0.36,
    },
}


def generate_prices(base_price, periods=180):
    returns = np.random.normal(0.0007, 0.018, periods)
    prices = base_price * np.exp(np.cumsum(returns))
    return prices


def technical_analysis(prices):
    series = pd.Series(prices)

    sma20 = series.rolling(20).mean().iloc[-1]
    sma50 = series.rolling(50).mean().iloc[-1]

    delta = series.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()

    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi_value = float(rsi.iloc[-1])

    volatility = float(series.pct_change().std() * np.sqrt(252) * 100)

    return {
        "sma20": sma20,
        "sma50": sma50,
        "rsi": rsi_value,
        "volatility": volatility
    }


def investment_dna(data, tech):
    growth = min(max(data["revenue_growth"] * 3.5, 0), 100)

    quality = min(
        max((data["roe"] * 3) + (30 if data["debt"] < 0.3 else 15), 0),
        100
    )

    momentum = min(
        max(50 + (tech["rsi"] - 50) * 1.5, 0),
        100
    )

    valuation = min(
        max(100 - data["pe"] * 2.0, 0),
        100
    )

    risk = min(
        max(tech["volatility"] * 3, 0),
        100
    )

    stability = 100 - risk

    return {
        "Growth": growth,
        "Quality": quality,
        "Momentum": momentum,
        "Valuation": valuation,
        "Risk": risk,
        "Stability": stability
    }


def create_chart(prices, title):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=prices,
            mode="lines",
            name="Price",
            line=dict(width=2)
        )
    )

    series = pd.Series(prices)

    fig.add_trace(
        go.Scatter(
            y=series.rolling(20).mean(),
            mode="lines",
            name="20D Trend",
            line=dict(width=1)
        )
    )

    fig.update_layout(
        title=title,
        height=430,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h")
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ◈ AUREX AI")

    st.caption("Autonomous Universal Research & EXecution Intelligence")

    st.divider()

    page = st.radio(
        "COMMAND CENTER",
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

    st.divider()

    st.caption("SYSTEM")

    st.success("● Research Engine Online")

    st.caption("API KEY: NOT REQUIRED")

    st.divider()

    st.caption(
        "AUREX AI is a research prototype. "
        "Demo data is used in this version."
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <span class="badge">AUREX AI • RESEARCH OS</span>
    <h1>Financial Intelligence, Reimagined.</h1>
    <p>
        Explore markets, companies, strategies, portfolios and risk
        through one analytical workspace.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# COMMAND CENTER
# =========================================================

if page == "◈ Command Center":

    st.markdown("## ◈ Command Center")

    st.markdown(
        "A unified workspace for investment research and market analysis."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Research Engine</div>
        <div class="metric-value">ONLINE</div>
        <div class="metric-small">Core analytical modules active</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">API Dependency</div>
        <div class="metric-value">ZERO</div>
        <div class="metric-small">V1 operates without API keys</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Research Modules</div>
        <div class="metric-value">8</div>
        <div class="metric-small">Integrated analytical areas</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Mode</div>
        <div class="metric-value">LAB</div>
        <div class="metric-small">Research & simulation environment</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 🔎 Start a Research Mission")

    selected = st.selectbox(
        "Select an asset",
        list(stocks.keys())
    )

    if st.button("🚀 Launch Research Mission", use_container_width=True):

        data = stocks[selected]
        prices = generate_prices(data["price"])
        tech = technical_analysis(prices)
        dna = investment_dna(data, tech)

        st.session_state["selected"] = selected
        st.session_state["prices"] = prices
        st.session_state["tech"] = tech
        st.session_state["dna"] = dna

        st.success(f"Research mission launched for {selected}")

    st.markdown("""
    <div class="disclaimer">
    ⚠️ AUREX AI is an analytical research prototype. It does not
    guarantee returns, predict markets with certainty, or constitute
    personalized financial advice.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# AI RESEARCH LAB
# =========================================================

elif page == "🧠 AI Research Lab":

    st.markdown("## 🧠 AI Research Lab")

    selected = st.selectbox(
        "Research target",
        list(stocks.keys())
    )

    data = stocks[selected]
    prices = generate_prices(data["price"])
    tech = technical_analysis(prices)

    question = st.text_area(
        "Research Question",
        placeholder="Example: What are the major factors I should investigate before considering this company?"
    )

    if st.button("🧠 Generate Research Report", use_container_width=True):

        st.markdown("### Research Intelligence")

        st.markdown(f"""
        <div class="research-box">
        <h3>{selected}</h3>
        <p>
        Sector: <b>{data["sector"]}</b><br>
        Reference price: <b>₹{data["price"]:,.2f}</b>
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📌 Business Snapshot")

        st.write(
            f"{selected} is represented in this prototype as a "
            f"{data['sector']} company. Key research variables include "
            f"growth, profitability, valuation, leverage and market behaviour."
        )

        st.markdown("### 📈 Market Behaviour")

        col1, col2, col3 = st.columns(3)

        col1.metric("RSI", f"{tech['rsi']:.1f}")
        col2.metric("Volatility", f"{tech['volatility']:.1f}%")
        col3.metric("20D Average", f"₹{tech['sma20']:,.2f}")

        st.markdown("### 🐂 Bull Scenario")

        st.write(
            "Potential upside drivers could include stronger revenue growth, "
            "improving profitability, favourable sector conditions and "
            "positive changes in investor expectations."
        )

        st.markdown("### ⚖️ Base Scenario")

        st.write(
            "A continuation scenario would depend on whether the company "
            "maintains its current operating performance while valuation "
            "and market conditions remain broadly stable."
        )

        st.markdown("### 🐻 Bear Scenario")

        st.write(
            "Potential downside factors could include slowing growth, "
            "margin pressure, rising leverage, weaker industry conditions "
            "or a decline in market sentiment."
        )

        st.markdown("### 🔍 Questions Worth Investigating")

        questions = [
            "Is revenue growth sustainable?",
            "How has profitability changed over multiple years?",
            "Is the current valuation supported by business performance?",
            "What are the company's major competitive risks?",
            "How sensitive is the company to economic conditions?",
            "What could invalidate the investment thesis?"
        ]

        for q in questions:
            st.write("• " + q)


# =========================================================
# MARKET INTELLIGENCE
# =========================================================

elif page == "📊 Market Intelligence":

    st.markdown("## 📊 Market Intelligence")

    selected = st.selectbox(
        "Asset",
        list(stocks.keys())
    )

    data = stocks[selected]
    prices = generate_prices(data["price"])
    tech = technical_analysis(prices)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Reference Price", f"₹{data['price']:,.2f}")
    c2.metric("Sector", data["sector"])
    c3.metric("P/E", f"{data['pe']:.1f}")
    c4.metric("Revenue Growth", f"{data['revenue_growth']:.1f}%")

    st.plotly_chart(
        create_chart(prices, f"{selected} — Simulated Price History"),
        use_container_width=True
    )

    st.markdown("### Market Variables")

    df = pd.DataFrame({
        "Variable": [
            "20-Day Average",
            "50-Day Average",
            "RSI",
            "Annualized Volatility"
        ],
        "Value": [
            f"₹{tech['sma20']:,.2f}",
            f"₹{tech['sma50']:,.2f}",
            f"{tech['rsi']:.1f}",
            f"{tech['volatility']:.1f}%"
        ]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TECHNICAL LAB
# =========================================================

elif page == "📈 Technical Laboratory":

    st.markdown("## 📈 Technical Laboratory")

    selected = st.selectbox(
        "Select asset",
        list(stocks.keys())
    )

    data = stocks[selected]
    prices = generate_prices(data["price"])
    tech = technical_analysis(prices)

    st.plotly_chart(
        create_chart(prices, f"{selected} Technical Chart"),
        use_container_width=True
    )

    a, b, c = st.columns(3)

    a.metric("RSI", f"{tech['rsi']:.1f}")
    b.metric("20D MA", f"₹{tech['sma20']:,.2f}")
    c.metric("50D MA", f"₹{tech['sma50']:,.2f}")

    st.markdown("### Interpretation")

    if tech["rsi"] > 70:
        st.info(
            "RSI is relatively high. This indicates strong recent price "
            "momentum; it does not by itself predict a future decline."
        )
    elif tech["rsi"] < 30:
        st.info(
            "RSI is relatively low. This indicates weak recent momentum; "
            "it does not by itself predict a future rebound."
        )
    else:
        st.info(
            "RSI is in a middle range, indicating neither an extreme "
            "high nor extreme low based on this indicator."
        )


# =========================================================
# PORTFOLIO
# =========================================================

elif page == "💼 Portfolio Intelligence":

    st.markdown("## 💼 Portfolio Intelligence")

    st.write(
        "Build a hypothetical portfolio and inspect concentration and exposure."
    )

    portfolio = {}

    for stock in stocks:

        portfolio[stock] = st.slider(
            stock,
            min_value=0,
            max_value=100,
            value=25,
            step=5
        )

    total = sum(portfolio.values())

    st.metric("Total Allocation", f"{total}%")

    if total > 0:

        normalized = {
            k: (v / total) * 100
            for k, v in portfolio.items()
            if v > 0
        }

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(normalized.keys()),
                    values=list(normalized.values()),
                    hole=0.55
                )
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Portfolio Structure")

        for stock, weight in normalized.items():
            st.write(f"**{stock}** — {weight:.1f}%")

        largest = max(normalized, key=normalized.get)

        st.info(
            f"Largest allocation: {largest} at {normalized[largest]:.1f}%. "
            "Consider how concentration affects portfolio risk."
        )


# =========================================================
# STRATEGY LAB
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

    starting_capital = st.number_input(
        "Starting Capital",
        min_value=10000,
        max_value=10000000,
        value=100000,
        step=10000
    )

    fast_window = st.slider(
        "Fast Moving Average",
        5,
        50,
        20
    )

    slow_window = st.slider(
        "Slow Moving Average",
        20,
        150,
        50
    )

    if fast_window >= slow_window:
        st.warning("Fast moving average must be smaller than slow moving average.")

    else:

        data = stocks[selected]
        prices = generate_prices(data["price"], 500)

        df = pd.DataFrame({"Price": prices})

        df["Fast"] = df["Price"].rolling(fast_window).mean()
        df["Slow"] = df["Price"].rolling(slow_window).mean()

        df["Signal"] = np.where(
            df["Fast"] > df["Slow"],
            1,
            0
        )

        df["Returns"] = df["Price"].pct_change()

        df["Strategy"] = df["Returns"] * df["Signal"].shift(1)

        df["Equity"] = (
            1 + df["Strategy"].fillna(0)
        ).cumprod() * starting_capital

        final_value = df["Equity"].iloc[-1]

        total_return = (
            (final_value / starting_capital) - 1
        ) * 100

        max_drawdown = (
            df["Equity"] / df["Equity"].cummax() - 1
        ).min() * 100

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Ending Value",
            f"₹{final_value:,.0f}"
        )

        c2.metric(
            "Historical Return",
            f"{total_return:.2f}%"
        )

        c3.metric(
            "Max Drawdown",
            f"{max_drawdown:.2f}%"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=df["Equity"],
                mode="lines",
                name="Strategy Equity"
            )
        )

        fig.update_layout(
            title="Historical Strategy Simulation",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.warning(
            "This is a historical simulation using generated demonstration "
            "data. It is not evidence of future performance."
        )


# =========================================================
# RISK OBSERVATORY
# =========================================================

elif page == "⚠️ Risk Observatory":

    st.markdown("## ⚠️ Risk Observatory")

    selected = st.selectbox(
        "Asset",
        list(stocks.keys())
    )

    data = stocks[selected]
    prices = gen
