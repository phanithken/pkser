import os
import re
import gzip
import argparse
from datetime import datetime, timedelta
import pandas as pd

# Set up argument parser
parser = argparse.ArgumentParser(description="Extract page views from Nginx logs")
parser.add_argument("log_dir", help="The path to the log directory.")
parser.add_argument("--start_date", help="Start date in YYYY-MM-DD format", type=str)
parser.add_argument("--end_date", help="End date in YYYY-MM-DD format", type=str)
args = parser.parse_args()

log_dir = args.log_dir
page_accesses = {}

# Regex to parse log lines
log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>[A-Z]+) (?P<url>\S+) HTTP/\d.\d" (?P<status>\d{3}) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"')

# Updated regex to identify pages (including dynamic paths but excluding static resources)
page_pattern = re.compile(r'^/(?!admin/)([^.]+)$')
exclude_pattern = re.compile(r'\.(css|js|jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot|json|xml|map|php)$')

# Function to check if a URL matches any of the patterns
def is_valid_page(url):
    return page_pattern.match(url) is not None and exclude_pattern.search(url) is None

def process_log_file(file_path, start_date, end_date):
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt') as file:
            process_lines(file, start_date, end_date)
    else:
        with open(file_path, 'r') as file:
            process_lines(file, start_date, end_date)

def process_lines(file, start_date, end_date):
    for line in file:
        match = log_pattern.match(line)
        if match and match.group('status') == '200':  # Filter for successful requests
            date_str = match.group('date')
            date = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z")

            if start_date <= date <= end_date:
                url = match.group('url')
                if is_valid_page(url):
                    if url in page_accesses:
                        page_accesses[url] += 1
                    else:
                        page_accesses[url] = 1

# Parse date arguments or use last month as default
if args.start_date and args.end_date:
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
else:
    today = datetime.now()
    start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    end_date = today.replace(day=1) - timedelta(days=1)

# Convert to timezone-aware datetime objects (assuming UTC)
start_date = start_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
end_date = end_date.replace(hour=23, minute=59, second=59, tzinfo=datetime.now().astimezone().tzinfo)

print(f"Processing logs from {start_date} to {end_date}")

# Process all log files in the directory
for log_file in os.listdir(log_dir):
    log_file_path = os.path.join(log_dir, log_file)
    process_log_file(log_file_path, start_date, end_date)

# Convert the results to the DataFrame
df = pd.DataFrame(list(page_accesses.items()), columns=['Page', 'Access Count'])

# Sort the DataFrame by Access Count in descending order
df = df.sort_values('Access Count', ascending=False)

# Write the DataFrame to an Excel file
output_file = f'page_accesses_{start_date.date()}_{end_date.date()}.xlsx'
df.to_excel(output_file, index=False)

print(f"Page access counts have been written to {output_file}")