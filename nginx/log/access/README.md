# Nginx Log Analyzer

This project is designed to analyze Nginx access logs and extract useful insights, such as page view counts. The current version includes a script to count page accesses and export the results to an Excel file.

## Features

- **Page Views Extraction**: Extract the number of accesses to each page from Nginx access logs and export the results to an Excel file.
- **Support for Compressed Logs**: The script handles both compressed (`.gz`) and uncompressed log files.

## Folder Structure
- **`page_views_extractor.py`**: The main script for extracting page view counts from the access logs.
- **`requirements.txt`**: A file listing the Python dependencies required for running the script.

## Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

## Installation

1. Clone the repository or download the script files.
2. Navigate to the `access/` directory where `requirements.txt` is located.
3. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the `access/` directory:

    ```bash
    cd nginx/log/access
    ```

2. Run the script:

    ```bash
    python page_views_extractor.py
    ```

3. When prompted, enter the path to the directory containing your Nginx log files. For example:

    ```plaintext
    Please enter the path to your log directory: ./logs
    ```

4. The script will process all the log files in the specified directory and output an Excel file named `page_accesses.xlsx` containing the page view counts.

## Future Features

This project is actively being developed, and we plan to add the following features:

- **Geolocation Analysis**: Determine the geographic location of visitors.
- **Error Rate Calculation**: Identify and calculate the rate of HTTP errors (e.g., 404, 500).
- **Traffic Source Analysis**: Analyze the traffic sources (e.g., direct, referral, search engines).
- **Time-based Analysis**: Provide insights into traffic patterns over different time periods.
- **Visualization**: Create graphs and charts for better data visualization.

## Contributing

We welcome contributions from the community! If you have any ideas or suggestions, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.