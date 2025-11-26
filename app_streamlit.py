import math
from datetime import date
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from backtest import backtest_portfolio, compute_metrics
from data import get_price_data

st.set_page_config(
    page_title="Market Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_TICKERS = ["AAPL", "OPEN", "TSLA", "SPY"]
POPULAR_TICKERS = sorted(
    set(
        DEFAULT_TICKERS
        + [
            "MSFT",
            "NVDA",
            "META",
            "AMZN",
            "GOOGL",
            "NFLX",
            "QQQ",
            "AMD",
            "JPM",
            "V",
            "MA",
            "DIS",
            "XOM",
            "CVX",
            "ARKK",
            "BA",
        ]
    )
)


@st.cache_data(show_spinner=False)
def load_price_data(tickers: Sequence[str], start: str, end: str) -> pd.DataFrame:
    """Cached wrapper around `get_price_data`."""
    if not tickers:
        return pd.DataFrame()

    # yfinance expects either a string ticker or a list; convert Sequence to list
    data = get_price_data(list(tickers), start=start, end=end)
    if isinstance(data, pd.Series):
        # Ensure single ticker responses are DataFrames
        data = data.to_frame(name=tickers[0])

    return data


def format_metric_value(metric: str, value: float) -> str:
    """Create human-readable strings for metric values."""
    percentage_metrics = {"total_return", "annual_return", "annual_vol", "max_drawdown"}
    if metric in percentage_metrics:
        return f"{value:.2%}"

    if metric == "sharpe":
        return f"{value:.4f}" if not math.isnan(value) else "N/A"

    return f"{value:.4f}"


def compute_drawdown(curve: pd.Series) -> pd.Series:
    running_max = curve.cummax()
    drawdown = curve / running_max - 1
    return drawdown.fillna(0)


def monthly_returns(returns: pd.Series) -> pd.Series:
    monthly = (1 + returns).resample("M").prod() - 1
    return monthly.dropna()


def render_equity_curve_chart(
    portfolio_curve: pd.Series,
    benchmark_curve: Optional[pd.Series],
    tickers: List[str],
    start: str,
    end: str,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        portfolio_curve.index,
        portfolio_curve.values,
        label=f"Portfolio ({', '.join(tickers)})",
        color="#2E86AB",
        linewidth=2,
    )

    if benchmark_curve is not None:
        ax.plot(
            benchmark_curve.index,
            benchmark_curve.values,
            label="SPY Benchmark",
            color="#A23B72",
            linestyle="--",
            linewidth=2,
        )

    ax.set_title(f"Equity Curve • {start} → {end}")
    ax.set_ylabel("Portfolio Value ($)")
    ax.grid(alpha=0.3, linestyle="--")
    ax.legend()
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
    )
    fig.autofmt_xdate()
    st.pyplot(fig)
    plt.close(fig)


def render_drawdown_chart(
    portfolio_curve: pd.Series,
    benchmark_curve: Optional[pd.Series],
) -> None:
    portfolio_dd = compute_drawdown(portfolio_curve) * 100
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(
        portfolio_dd.index,
        portfolio_dd.values,
        0,
        alpha=0.3,
        color="#2E86AB",
        label="Portfolio Drawdown",
    )
    ax.plot(portfolio_dd.index, portfolio_dd.values, color="#2E86AB", linewidth=1.5)

    if benchmark_curve is not None:
        benchmark_dd = compute_drawdown(benchmark_curve) * 100
        ax.fill_between(
            benchmark_dd.index,
            benchmark_dd.values,
            0,
            alpha=0.2,
            color="#A23B72",
            label="SPY Drawdown",
        )
        ax.plot(
            benchmark_dd.index,
            benchmark_dd.values,
            color="#A23B72",
            linewidth=1.2,
            linestyle="--",
        )

    ax.set_title("Drawdown Comparison")
    ax.set_ylabel("Drawdown (%)")
    ax.set_ylim(bottom=min(portfolio_dd.min() - 5, -5), top=5)
    ax.grid(alpha=0.3, linestyle="--")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)
    plt.close(fig)


def render_monthly_returns_chart(
    portfolio_returns: pd.Series, benchmark_returns: Optional[pd.Series]
) -> None:
    portfolio_monthly = monthly_returns(portfolio_returns)
    data = pd.DataFrame({"Portfolio": portfolio_monthly})

    if benchmark_returns is not None:
        benchmark_monthly = monthly_returns(benchmark_returns)
        data["SPY"] = benchmark_monthly

    data = data.fillna(0)
    months = data.index
    x = np.arange(len(months))

    fig, ax = plt.subplots(figsize=(11, 4))

    width = 0.35 if data.shape[1] > 1 else 0.6
    ax.bar(
        x - width / 2 if data.shape[1] > 1 else x,
        data["Portfolio"].values * 100,
        width,
        label="Portfolio",
        color="#2E86AB",
    )

    if "SPY" in data.columns:
        ax.bar(
            x + width / 2,
            data["SPY"].values * 100,
            width,
            label="SPY",
            color="#A23B72",
        )

    ax.axhline(0, color="#444", linewidth=0.8)
    ax.set_ylabel("Monthly Return (%)")
    ax.set_title("Monthly Returns")
    ax.set_xticks(x)
    ax.set_xticklabels([month.strftime("%Y-%m") for month in months], rotation=45)
    ax.grid(axis="y", alpha=0.2)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


st.title("📊 Market Simulator")
st.caption("Backtest custom equity portfolios and benchmark them against the S&P 500.")

with st.sidebar:
    st.header("Backtest Controls")
    st.caption("Adjust the inputs below — the analysis refreshes automatically.")

    tickers = st.multiselect(
        "Portfolio tickers",
        options=POPULAR_TICKERS,
        default=DEFAULT_TICKERS,
        help="Pick the securities that make up your portfolio.",
    )

    custom_tickers_input = st.text_input(
        "Add custom tickers",
        placeholder="e.g. SHOP, SQ, IBM",
        help="Comma-separated list. These will be appended to the selection above.",
    )

    if custom_tickers_input:
        custom = [
            ticker.strip().upper()
            for ticker in custom_tickers_input.split(",")
            if ticker.strip()
        ]
        for ticker in custom:
            if ticker not in tickers:
                tickers.append(ticker)

    start_date = st.date_input(
        "Start date",
        value=date(2020, 1, 1),
        help="We recommend at least one full year for stable metrics.",
    )
    end_date = st.date_input("End date", value=date(2025, 1, 1))

    initial_investment = st.number_input(
        "Initial investment ($)",
        min_value=1000.0,
        max_value=5_000_000.0,
        value=10_000.0,
        step=1_000.0,
        format="%.2f",
    )

    weights_map: Optional[dict[str, float]] = None
    use_custom_weights = False
    if tickers:
        st.divider()
        use_custom_weights = st.checkbox(
            "Use custom portfolio weights",
            value=False,
            help="Specify allocation percentages per ticker (defaults to equal weights).",
        )

        if use_custom_weights:
            st.caption("Set allocation percentages (0-100%). They will be normalized automatically.")
            weights_map = {}
            total_pct = 0.0
            default_pct = round(100.0 / len(tickers), 1)

            for idx, ticker in enumerate(tickers):
                pct = st.number_input(
                    f"{ticker} weight (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=default_pct if idx == 0 else 0.0,
                    step=1.0,
                    key=f"weight_{ticker}",
                    format="%.1f",
                )
                weights_map[ticker] = pct / 100.0
                total_pct += pct

            if abs(total_pct - 100.0) <= 0.5:
                st.success(f"Total weights: {total_pct:.1f}%")
            else:
                st.warning(
                    f"Total weights: {total_pct:.1f}% (will be normalized to 100%)."
                )

    include_spy = st.checkbox("Compare against SPY benchmark", value=True)
    show_monthly = st.checkbox("Show monthly returns breakdown", value=True)
    show_data_preview = st.checkbox("Show price data preview", value=False)

st.divider()

if not tickers:
    st.warning("Select at least one ticker to run the backtest.")
elif start_date >= end_date:
    st.error("`End date` must be after `Start date`.")
else:
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    try:
        with st.spinner("Downloading price data and running backtest..."):
            prices = load_price_data(tuple(tickers), start_str, end_str)

        if prices.empty:
            st.error("No price data returned for the selected tickers/dates.")
            st.stop()

        available_columns = [col for col in prices.columns if col in tickers]
        missing_tickers = [ticker for ticker in tickers if ticker not in prices.columns]

        if missing_tickers:
            st.warning(
                f"The following tickers were skipped because no data was found: "
                f"{', '.join(missing_tickers)}"
            )

        if not available_columns:
            st.error("No valid tickers remain after filtering missing data.")
            st.stop()

        prices = prices[available_columns]

        if use_custom_weights and weights_map:
            raw_weights = np.array(
                [weights_map.get(col, 0.0) for col in available_columns], dtype=float
            )
            total_raw = raw_weights.sum()
            if total_raw == 0:
                st.error(
                    "Custom weights total 0%. Adjust the sliders so the total is greater than zero."
                )
                st.stop()
            weights = (raw_weights / total_raw).tolist()
            st.info(
                "**Portfolio allocation:** "
                + ", ".join(
                    f"{ticker}: {weight:.1%}"
                    for ticker, weight in zip(available_columns, weights)
                )
            )
        else:
            weights = [1 / len(available_columns)] * len(available_columns)

        equity_curve, portfolio_returns = backtest_portfolio(
            prices, weights, initial_investment
        )
        portfolio_metrics = compute_metrics(equity_curve, portfolio_returns)

        spy_equity_curve: Optional[pd.Series] = None
        spy_returns: Optional[pd.Series] = None
        spy_metrics = None

        if include_spy:
            spy_prices = load_price_data(("SPY",), start_str, end_str)
            spy_equity_curve, spy_returns = backtest_portfolio(
                spy_prices, [1.0], initial_investment
            )
            spy_metrics = compute_metrics(spy_equity_curve, spy_returns)

    except Exception as exc:  # noqa: BLE001
        st.error(f"Backtest failed: {exc}")
        st.stop()

    st.subheader("Performance Overview")
    perf_cols = st.columns(3)
    perf_cols[0].metric(
        "Final portfolio value",
        f"${equity_curve.iloc[-1]:,.0f}",
        delta=f"{portfolio_metrics['total_return']:.2%}",
    )

    if spy_equity_curve is not None:
        delta_vs_spy = equity_curve.iloc[-1] - spy_equity_curve.iloc[-1]
        perf_cols[1].metric(
            "Final SPY value",
            f"${spy_equity_curve.iloc[-1]:,.0f}",
            delta=f"{spy_metrics['total_return']:.2%}",
        )
        perf_cols[2].metric(
            "Outperformance vs SPY",
            f"${delta_vs_spy:,.0f}",
            delta=f"{(equity_curve.iloc[-1] / spy_equity_curve.iloc[-1] - 1) * 100:+.2f}%",
        )
    else:
        perf_cols[1].metric(
            "Annualized return",
            f"{portfolio_metrics['annual_return']:.2%}",
        )
        perf_cols[2].metric(
            "Max drawdown",
            f"{portfolio_metrics['max_drawdown']:.2%}",
        )

    metrics_df = pd.DataFrame({"Portfolio": portfolio_metrics})
    if spy_metrics:
        metrics_df["SPY"] = pd.Series(spy_metrics)

    formatted_metrics = metrics_df.copy()
    for column in formatted_metrics.columns:
        formatted_metrics[column] = [
            format_metric_value(metric, value)
            for metric, value in zip(metrics_df.index, metrics_df[column])
        ]

    st.dataframe(
        formatted_metrics,
        use_container_width=True,
    )

    st.subheader("Equity Curve")
    render_equity_curve_chart(
        equity_curve,
        benchmark_curve=spy_equity_curve if include_spy else None,
        tickers=available_columns,
        start=start_str,
        end=end_str,
    )

    st.subheader("Drawdown Analysis")
    render_drawdown_chart(
        equity_curve,
        benchmark_curve=spy_equity_curve if include_spy else None,
    )

    if show_monthly:
        st.subheader("Monthly Returns")
        render_monthly_returns_chart(
            portfolio_returns, spy_returns if include_spy else None
        )

    with st.expander("Download results", expanded=False):
        results_df = pd.DataFrame({"Portfolio": equity_curve})
        if spy_equity_curve is not None:
            results_df["SPY"] = spy_equity_curve
        csv = results_df.to_csv().encode("utf-8")
        st.download_button(
            "Download equity curves (CSV)",
            data=csv,
            file_name=f"market_simulator_{start_str}_{end_str}.csv",
            mime="text/csv",
        )

    if show_data_preview:
        st.subheader("Price Data Preview")
        st.dataframe(prices.tail(), use_container_width=True)

