# Stock Data Notifier

This project fetches stock market data for specified symbols using the RealStonks API, stores the data in a DataFrame, and sends email notifications with the latest stock data. All of this automated by a cron job.

## Project Structure

- `main.py`: Main Python script that fetches stock data, processes it, and sends email notifications.
- `credentials.py`: Script to store and modify credentials for API access and email notifications.
- `cronjob.sh`: Bash script to set up a cron job to run main.py every 5 minutes.

## Dependencies

This project requires the following dependencies:

- Python 3.x
- Pandas
- Requests
- smtplib (for sending emails)
- email.mime (for constructing email messages)

## Obtaining the RealStonks API Key

To use the RealStonks API, you'll need to obtain an API key from RapidAPI. Follow the steps below to get your API key:

1. Visit the RealStonks API on RapidAPI.

2. Sign in or create a new RapidAPI account.

3. Subscribe to the RealStonks API to get your API key.

4. Once subscribed, you can find your API key in the API dashboard.

> Make sure to keep your API key secure and never share it publicly.

## Usage

1. Clone this repository:

```bash
    git clone https://github.com/caidam/stock-data-notifier.git
    cd stock-data-notifier 
```

2. Update `credentials.py` with your RealStonks API key, email sender, receiver, and Google app password.

3. Run the main script `main.py` to fetch stock data, append it to the existing DataFrame (if any), and send email notifications:

```bash
    python main.py
```

This script fetches stock data for specified symbols (`symbols` list in `main.py`) using the RealStonks API, appends the data to a DataFrame, and sends an email notification.

4. Optionally, set up a cron job to run `main.py` every 5 minutes for continuous data fetching and notification.

## Note

- Ensure that you have updated the symbols list in main.py with the desired stock symbols.
- The fetched data is stored in a CSV file named stocks.csv.

Feel free to modify the stock symbols, frequency of data fetching, and other configurations to suit your requirements.

> ## How to set up a Cron Job

### Step 1: Open the Crontab Configuration

Open the crontab configuration by running the following command in your terminal:

```bash
    crontab -e
```

This will open the default text editor for editing the crontab file.

### Step 2: Add the Cron Job Entry

Add a new line to the crontab file for the desired scheduling of the `main.py` script. The general format for a cron job entry is as follows:

```bash
    * * * * * command_to_be_executed
    - - - - -
    | | | | |
    | | | | +----- Day of the week (0 - 7) (Both 0 and 7 represent Sunday)
    | | | +------- Month (1 - 12)
    | | +--------- Day of the month (1 - 31)
    | +----------- Hour (0 - 23)
    +------------- Minute (0 - 59)
```

For example, to run the main.py script every 5 minutes, add the following line:

```bash
    */5 * * * * python /path/to/your/repo/main.py
```

Replace `/path/to/your/repo` with the actual path to the directory containing the `main.py` script.

### Step 3: Save and Exit

Save the crontab file and exit the text editor. The changes will take effect immediately.

Now, the `main.py` script will be executed every 5 minutes based on the specified cron job configuration.

Feel free to adjust the timing and frequency of the cron job according to your requirements.
