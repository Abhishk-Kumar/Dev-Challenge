# Task 2 solution 

# Import necessary libraries
import pandas as pd

# 1. Prompt user to select a derivative type
def get_derivative_type():
    derivatives = ["Nifty", "BankNifty", "FinNifty", "BankEx"]
    print("Select Derivative Type:")
    for i, d in enumerate(derivatives):
        print(f"{i+1}. {d}")
    choice = int(input("Enter the number corresponding to your choice: ")) - 1
    return derivatives[choice]

# 2. Allow selection of multiple timeframes
def get_timeframes():
    timeframes = ["1 min", "5 min", "1 hour", "1 day"]
    print("Select Timeframes (comma separated):")
    for i, t in enumerate(timeframes):
        print(f"{i+1}. {t}")
    choices = input("Enter the numbers corresponding to your choices: ").split(',')
    return [timeframes[int(c) - 1] for c in choices]

# 3. Ask user for expiry date if derivative type is options/futures
def get_expiry_date():
    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
    return expiry_date

# 4. Offer predefined strategies or allow custom strategy input
def get_strategy():
    strategies = ["Moving Average Crossover", "RSI", "Bollinger Bands", "Custom"]
    print("Select Trading Strategy:")
    for i, s in enumerate(strategies):
        print(f"{i+1}. {s}")
    choice = int(input("Enter the number corresponding to your choice: ")) - 1
    if strategies[choice] == "Custom":
        return input("Enter your custom strategy: ")
    return strategies[choice]

# 5. Validate the user inputs and gather them
def get_user_input():
    derivative_type = get_derivative_type()  # Get derivative type from user
    timeframes = get_timeframes()  # Get timeframes from user
    expiry_date = get_expiry_date()  # Get expiry date for options/futures
    strategy = get_strategy()  # Get the selected trading strategy
    return derivative_type, timeframes, expiry_date, strategy

# 6. Filter data based on user-selected derivative, timeframes, and expiry
def filter_data(df, derivative_type, expiry_date):
    filtered_data = df[(df['derivative_type'] == derivative_type) & (df['expiry_date'] == expiry_date)]
    return filtered_data

# 7. Apply selected strategy dynamically
def apply_strategy(filtered_data, strategy):
    print(f"Applying {strategy} strategy on the filtered data.")
    # Strategy logic would go here, depending on the strategy chosen by the user

# Main function to demonstrate input handling
def main():
    df = pd.DataFrame()  # Example data frame placeholder
    derivative_type, timeframes, expiry_date, strategy = get_user_input()  # Gather user inputs
    filtered_data = filter_data(df, derivative_type, expiry_date)  # Filter data based on inputs
    apply_strategy(filtered_data, strategy)  # Apply selected strategy

if __name__ == "__main__":
    main()
