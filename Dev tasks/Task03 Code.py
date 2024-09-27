# Task 3 solution 
import pandas as pd

# 1. Calculate moving averages for the Moving Average Crossover strategy
def calculate_moving_average(df, short_window=50, long_window=200):
    df['short_ma'] = df['close'].rolling(window=short_window, min_periods=1).mean()  # Short-term MA
    df['long_ma'] = df['close'].rolling(window=long_window, min_periods=1).mean()    # Long-term MA

# 2. Generate buy/sell signals based on the Moving Average Crossover
def moving_average_crossover(df):
    df['signal'] = 0  # Initialize signal column
    df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy signal
    df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell signal

# 3. Calculate RSI for RSI strategy
def calculate_rsi(df, window=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()  # Average gain
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()  # Average loss
    rs = gain / loss  # Relative Strength
    df['rsi'] = 100 - (100 / (1 + rs))  # RSI formula

# 4. Generate buy/sell signals based on RSI
def rsi_strategy(df):
    df['signal'] = 0  # Initialize signal column
    df['signal'][df['rsi'] < 30] = 1  # Buy signal
    df['signal'][df['rsi'] > 70] = -1  # Sell signal

# 5. Implement stop-loss logic
def apply_stop_loss(df, stop_loss_percent=0.02):
    df['stop_loss'] = df['close'] * (1 - stop_loss_percent)  # Calculate stop-loss based on percentage
    df['trailing_stop'] = df['close'].cummax() * (1 - stop_loss_percent)  # Trailing stop based on max close

# 6. Process multiple expiries and derivatives
def process_multiple_expiries(df, expiry_column='expiry_date'):
    current_expiry = df[expiry_column].min()  # Identify the current expiry contract
    filtered_df = df[df[expiry_column] == current_expiry]  # Filter data for the current expiry
    return filtered_df

# 7. Apply signal generation logic dynamically based on selected strategy
def generate_signals(df, strategy):
    if strategy == "Moving Average Crossover":
        calculate_moving_average(df)  # Calculate MAs for crossover strategy
        moving_average_crossover(df)  # Generate MA crossover signals
    elif strategy == "RSI":
        calculate_rsi(df)  # Calculate RSI for strategy
        rsi_strategy(df)  # Generate RSI-based signals

# 8. Main function to handle strategy implementation and signal generation
def main():
    # Example DataFrame placeholder
    df = pd.DataFrame({'close': [100, 102, 101, 104, 107], 'expiry_date': ['2024-09-01'] * 5})
    
    # Select strategy (can be based on user input in a real scenario)
    strategy = "Moving Average Crossover"
    
    # Step 1: Process expiry and filter data for current expiry
    df = process_multiple_expiries(df)
    
    # Step 2: Generate buy/sell signals based on the selected strategy
    generate_signals(df, strategy)
    
    # Step 3: Apply stop-loss logic to minimize risk
    apply_stop_loss(df)
    
    print(df)

if __name__ == "__main__":
    main()
