import os
import re
import gzip
import argparse
import pandas as pd

# Set up argument parser
parser = argparse.ArgumentParser(description="Extract page views from Nginx logs")
parser.add_argument("log_dir", help="The path to the log directory.")
args = parser.parse_args()

log_dir = args.log_dir
page_accesses = {}

# Regex to parse log lines
log_pattern = re.compile(r'(?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>[A-Z]+) (?P<url>\S+) HTTP/\d.\d" (?P<status>\d{3})')

# Regex to identify pages (excluding static resources)
page_pattern = re.compile(r'^/$|^/[^/?&]+(?:/[^\d][^/?&]*)?/?$')
exclude_pattern = re.compile(r'\.(css|js|jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot|json|xml|map|php)$')

# Function to check if a URL matches any of the patterns
def is_valid_page(url):
    return page_pattern.match(url) is not None and exclude_pattern.search(url) is None

def process_log_file(file_path):
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt') as file:
            process_lines(file)
    else:
        with open(file_path, 'r') as file:
            process_lines(file)

def process_lines(file):
    for line in file:
        match = log_pattern.match(line)
        if match and match.group('status') == '200': # Filter for successful requests
            url = match.group('url')
            if is_valid_page(url):
                if url in page_accesses:
                    page_accesses[url] += 1
                else:
                    page_accesses[url] = 1

# Process all log files in the directory
for log_file in os.listdir(log_dir):
    log_file_path = os.path.join(log_dir, log_file)
    process_log_file(log_file_path)

# Convert the results to the DataFrame
df = pd.DataFrame(list(page_accesses.items()), columns=['Page', 'Access Count'])

# Write the DataFrame to an Excel file
output_file = 'page_accesses.xlsx'
df.to_excel(output_file, index=False)

print(f"Page access counts have been written to {output_file}")