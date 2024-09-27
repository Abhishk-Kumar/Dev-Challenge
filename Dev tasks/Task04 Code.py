# Task 4 solution 

import pandas as pd

# 1. Resample data to different timeframes (1 min, 5 min, 1 hour, 1 day)
def resample_data(df, timeframe):
    if timeframe == '1 min':
        return df.resample('1T').mean()  # Resample to 1 minute intervals
    elif timeframe == '5 min':
        return df.resample('5T').mean()  # Resample to 5 minute intervals
    elif timeframe == '1 hour':
        return df.resample('1H').mean()  # Resample to 1 hour intervals
    elif timeframe == '1 day':
        return df.resample('1D').mean()  # Resample to 1 day intervals

# 2. Calculate backtest performance metrics like total profit/loss
def calculate_profit_loss(df):
    df['strategy_returns'] = df['signal'].shift(1) * (df['close'].pct_change())  # Calculate strategy returns
    total_profit_loss = df['strategy_returns'].cumsum().iloc[-1]  # Calculate cumulative profit/loss
    return total_profit_loss

# 3. Calculate win rate (percentage of profitable trades)
def calculate_win_rate(df):
    profitable_trades = df[df['strategy_returns'] > 0].shape[0]  # Count profitable trades
    total_trades = df['signal'].diff().abs().sum()  # Count total trades (buy/sell signals)
    return profitable_trades / total_trades if total_trades > 0 else 0

# 4. Calculate risk-adjusted metrics like Sharpe Ratio
def calculate_sharpe_ratio(df, risk_free_rate=0.01):
    excess_returns = df['strategy_returns'] - risk_free_rate / 252  # Calculate excess returns over risk-free rate
    return excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0  # Sharpe ratio formula

# 5. Calculate maximum drawdown to measure risk
def calculate_max_drawdown(df):
    cumulative_returns = (1 + df['strategy_returns']).cumprod()  # Calculate cumulative returns
    peak = cumulative_returns.cummax()  # Track the peak value
    drawdown = (cumulative_returns - peak) / peak  # Calculate drawdown from the peak
    return drawdown.min()  # Return maximum drawdown

# 6. Backtest the strategy for each timeframe and calculate metrics
def backtest_strategy(df, timeframes):
    results = {}
    for timeframe in timeframes:
        resampled_df = resample_data(df, timeframe)  # Resample data to the selected timeframe
        total_profit_loss = calculate_profit_loss(resampled_df)  # Calculate profit/loss
        win_rate = calculate_win_rate(resampled_df)  # Calculate win rate
        sharpe_ratio = calculate_sharpe_ratio(resampled_df)  # Calculate Sharpe ratio
        max_drawdown = calculate_max_drawdown(resampled_df)  # Calculate maximum drawdown
        results[timeframe] = {
            'Total Profit/Loss': total_profit_loss,
            'Win Rate': win_rate,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown
        }
    return results

# 7. Main function to run backtest across multiple timeframes
def main():
    # Example DataFrame placeholder with signals
    df = pd.DataFrame({'close': [100, 102, 101, 104, 107], 'signal': [1, -1, 1, 0, 1]},
                      index=pd.date_range('2024-09-01', periods=5, freq='1T'))
    
    timeframes = ['1 min', '5 min', '1 hour', '1 day']  # List of timeframes for backtesting
    results = backtest_strategy(df, timeframes)  # Backtest the strategy across different timeframes
    
    for timeframe, metrics in results.items():
        print(f"Results for {timeframe}:")
        print(f"Total Profit/Loss: {metrics['Total Profit/Loss']:.2f}")
        print(f"Win Rate: {metrics['Win Rate']:.2%}")
        print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown: {metrics['Max Drawdown']:.2%}")
        print("-" * 30)

if __name__ == "__main__":
    main()
