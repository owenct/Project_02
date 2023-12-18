import json
import numpy as np
import pandas as pd
import yfinance as yf

def calculate_portfolio_metrics(stock_ticker, short_window=20, long_window=100, initial_capital=100000, share_size=500):
    # Data Preparation
    getStockData = yf.Ticker(stock_ticker)
    df = pd.DataFrame(data=getStockData.history(period="max"))
    signals_df = df.copy()

    # Generate moving averages
    signals_df['SMA50'] = signals_df['Close'].rolling(window=short_window).mean()
    signals_df['SMA100'] = signals_df['Close'].rolling(window=long_window).mean()

    # Generate trading signals
    signals_df['Signal'] = 0.0
    signals_df['Signal'][short_window:] = np.where(
        signals_df['SMA50'][short_window:] > signals_df['SMA100'][short_window:], 1.0, 0.0
    )

    # Entry/Exit signals
    signals_df['Entry/Exit'] = signals_df['Signal'].diff()

    # Set initial capital
    signals_df['Position'] = share_size * signals_df['Signal']
    signals_df['Entry/Exit Position'] = signals_df['Position'].diff()
    signals_df['Portfolio Holdings'] = signals_df['Close'] * signals_df['Position']
    signals_df['Portfolio Cash'] = initial_capital - (signals_df['Close'] * signals_df['Entry/Exit Position']).cumsum()
    signals_df['Portfolio Total'] = signals_df['Portfolio Cash'] + signals_df['Portfolio Holdings']
    signals_df['Portfolio Daily Returns'] = signals_df['Portfolio Total'].pct_change()
    signals_df['Portfolio Cumulative Returns'] = (1 + signals_df['Portfolio Daily Returns']).cumprod() - 1

    # Portfolio-Level Risk/Reward Evaluation Metrics
    portfolio_evaluation_df = pd.DataFrame(index=["Annualized Return", "Cumulative Returns", "Annual Volatility", "Sharpe Ratio", "Sortino Ratio"],
                                           columns=["Backtest"])

    portfolio_evaluation_df.loc["Annualized Return"] = signals_df["Portfolio Daily Returns"].mean() * 252
    portfolio_evaluation_df.loc["Cumulative Returns"] = signals_df["Portfolio Cumulative Returns"][-1]
    portfolio_evaluation_df.loc["Annual Volatility"] = signals_df["Portfolio Daily Returns"].std() * np.sqrt(252)
    portfolio_evaluation_df.loc["Sharpe Ratio"] = (signals_df["Portfolio Daily Returns"].mean() * 252) / (signals_df["Portfolio Daily Returns"].std() * np.sqrt(252))

    # Sortino Ratio Calculation
    sortino_ratio_df = signals_df[["Portfolio Daily Returns"]].copy()
    sortino_ratio_df.loc[:, "Downside Returns"] = 0
    sortino_ratio_df.loc[sortino_ratio_df["Portfolio Daily Returns"] < 0, "Downside Returns"] = sortino_ratio_df["Portfolio Daily Returns"] ** 2

    annualized_return = sortino_ratio_df["Portfolio Daily Returns"].mean() * 252
    downside_standard_deviation = np.sqrt(sortino_ratio_df["Downside Returns"].mean()) * np.sqrt(252)
    sortino_ratio = annualized_return / downside_standard_deviation

    portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio

    return signals_df, portfolio_evaluation_df

# Example usage
stock_ticker = "MSFT"
short_window = 20
long_window = 100
initial_capital = 100000
share_size = 500

signals_df, portfolio_evaluation_df = calculate_portfolio_metrics(stock_ticker, short_window, long_window, initial_capital, share_size)

print("Signals DataFrame:")
print(signals_df.head(10))
print("\nPortfolio Evaluation DataFrame:")
print(json.dumps(portfolio_evaluation_df.to_json(orient = 'columns')) )
print(type(portfolio_evaluation_df))

