import os
import pandas as pd
import yfinance as yf
import hashlib
import re
from datetime import datetime

USER_DATA_FILE = "user.xlsx"
CSV_STORAGE_FOLDER = "stock_data"


def is_valid_email(email):
    """
    Validates an email address using regex.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def is_valid_password(password):
    """
    Validates password based on a simple policy:
    - At least 8 characters.
    - At least one letter and one number.
    """
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)


def hash_password(password):
    """
    Hashes a password using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email, password):
    """
    Registers a new user by adding their email and hashed password to the user.xlsx file.
    """
    if not is_valid_email(email):
        print("Invalid email format.")
        return

    if not is_valid_password(password):
        print("Password must be at least 8 characters long and include both letters and numbers.")
        return

    try:
        df = pd.read_excel(USER_DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Email", "Password"])

    if email.strip() in df["Email"].values:
        print("Email already registered.")
        return

    hashed_password = hash_password(password.strip())
    new_user = {"Email": email.strip(), "Password": hashed_password}
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_excel(USER_DATA_FILE, index=False)
    print("Registration successful!")


def authenticate_user(email, password):
    """
    Authenticates a user by verifying the provided email and password.
    """
    try:
        df = pd.read_excel(USER_DATA_FILE)
    except FileNotFoundError:
        print("No user data available. Please register first.")
        return False

    if email.strip() in df["Email"].values:
        hashed_password = hash_password(password.strip())
        stored_password = df.loc[df["Email"] == email.strip(), "Password"].values[0]
        if stored_password == hashed_password:
            print("\nLogin successful!\n")
            return True

    print("Invalid email or password.")
    return False


def validate_date_format(date_str):
    """
    Validates the format of a date string (YYYY-MM-DD).
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_closing_prices(ticker, start_date, end_date):
    """
    Fetches historical stock closing prices for a given ticker and date range.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty or "Close" not in data.columns:
            print(f"No data found for ticker {ticker} in the given date range.")
            return None
        return data["Close"]
    except Exception as e:
        print(f"Error fetching data for ticker {ticker}: {e}")
        return None


def analyze_closing_prices(data):
    """
    Analyzes stock closing prices for average, percentage change, and high/low points.
    """
    if data is None or data.empty:
        print("No data available for analysis.")
        return None

    avg_price = data.mean().item()
    first_price = data.iloc[0].item()
    last_price = data.iloc[-1].item()
    pct_change = ((last_price - first_price) / first_price) * 100
    highest_price = data.max().item()
    lowest_price = data.min().item()

    return {
        "Average Price": round(avg_price, 2),
        "Percentage Change (%)": round(pct_change, 2),
        "Highest Price": round(highest_price, 2),
        "Lowest Price": round(lowest_price, 2),
    }


def save_to_csv(data, email, ticker):
    """
    Saves the analysis results to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    os.makedirs(CSV_STORAGE_FOLDER, exist_ok=True)
    filename = f"{email.split('@')[0]}_{ticker}.csv"
    filepath = os.path.join(CSV_STORAGE_FOLDER, filename)

    df = pd.DataFrame(list(data.items()), columns=["Metric", "Value"])
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")


def read_from_csv(email):
    """
    Reads and displays previously saved data for the user.
    """
    os.makedirs(CSV_STORAGE_FOLDER, exist_ok=True)
    user_files = [f for f in os.listdir(CSV_STORAGE_FOLDER) if f.startswith(email.split("@")[0])]

    if not user_files:
        print("No saved data found.")
        return

    print("Available analysis files:")
    for i, file in enumerate(user_files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("Enter the file number to view: "))
        if 1 <= choice <= len(user_files):
            filepath = os.path.join(CSV_STORAGE_FOLDER, user_files[choice - 1])
            df = pd.read_csv(filepath)
            print(f"\nData from {user_files[choice - 1]}:\n")
            print(df.to_string(index=False))
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
