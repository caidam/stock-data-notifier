import requests
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import credentials

def get_market_data(symbol):
    """
    Fetch market data for a given stock symbol using the RealStonks API.

    Args:
        symbol (str): Stock symbol to fetch data for.

    Returns:
        dict or None: Market data for the specified symbol in JSON format,
                      or None if an error occurred during the API request.
    """
    # Construct the URL for the RealStonks API using the provided symbol
    url = f'https://realstonks.p.rapidapi.com/{symbol}'
    
    RAPIDAPIKEY = credentials.rapidapikey
    
    # Headers required for the RapidAPI request
    headers = {
      "X-RapidAPI-Key": RAPIDAPIKEY,  # Replace with your RapidAPI key
      "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
    }

    # Send a GET request to the RealStonks API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a dictionary and return it
        data = response.json()
        return data
    else:
        # Return None if an error occurred during the API request
        return None


def send_mail(df):
    """
    Send an email with stock data.

    Args:
        df (pandas.DataFrame): DataFrame containing stock data.

    Returns:
        None
    """
    # Sender's email information
    sender = credentials.sender

    # Recipient's email information
    receiver = credentials.receiver

    # Sender's email account password
    password = credentials.google_app_password

    # SMTP server configuration for Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Stock Data'

    # Convert DataFrame to a formatted string for the message body
    message = 'Stock Data:\n\n' + df.to_string(index=False)
    msg.attach(MIMEText(message))

    try:
        # Establish an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as mailserver:
            mailserver.starttls()  # Start a TLS encrypted connection
            mailserver.login(sender, password)
            mailserver.sendmail(sender, receiver, msg.as_string())
            print('Email sent successfully.')
    except smtplib.SMTPException as e:
        print('An error occurred while sending the email:', str(e))
    except Exception as e:
        print('An unexpected error occurred:', str(e))


def fetch_and_notify_stock_data(df, symbols):
    """
    Main function to continuously fetch stock market data for specified symbols
    and send email notifications with the latest data.

    Returns:
        None
    """

    # Initialize an empty DataFrame for the email
    df_mail = pd.DataFrame()

    # Iterate through each stock symbol
    for symbol in symbols:
        # Fetch market data for the current symbol
        data = get_market_data(symbol)

        # If data is successfully retrieved
        if data:
            # Create a temporary DataFrame with the fetched data
            temp_df = pd.DataFrame(data, index=[0])
            temp_df['symbol'] = symbol
            temp_df['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Concatenate the temporary DataFrame to the email DataFrame
            df_mail = pd.concat([df_mail, temp_df], ignore_index=True)
            time.sleep(1)  # Pause for a second between requests to the API

    # Try to access the existing DataFrame
    try:
        df  
    except NameError:
        # DataFrame does not exist, create an empty DataFrame
        df = pd.DataFrame()  # 

    # Concatenate the email DataFrame with the main DataFrame
    df = pd.concat([df, df_mail], ignore_index=True)

    # Save the updated DataFrame to a CSV file
    df.to_csv('stocks.csv')

    # Send an email with the latest data
    send_mail(df_mail.tail())

    # Print a message indicating the loop iteration
    print('Successfuly fetched data and notified by email')


if __name__ == "__main__":

    symbols = ['TSLA', 'MSFT', 'SPOT', 'UBER', 'AAPL']

    df = pd.DataFrame()

    fetch_and_notify_stock_data(df, symbols)