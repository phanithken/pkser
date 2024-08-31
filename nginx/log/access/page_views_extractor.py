import os
import re
import gzip
import pandas as pd

log_dir = input("Please enter the path to the log directory: ")
page_accesses = {}

# Regex to parse log lines
log_pattern = re.compile(r'(?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>[A-Z]+) (?P<url>\S+) HTTP/\d.\d" (?P<status>\d{3})')

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