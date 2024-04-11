### Objective
The goal was to create a Python script that fetches alert data from Red Hat Advanced Cluster Security API endpoint, formats this data, and then saves it in a CSV file.

### Key Steps

1. **Setting Up Environment Variables**:
   - The script reads the API bearer token (`ROX_API_TOKEN`) and the API endpoint (`ROX_ENDPOINT`) from environment variables.

2. **Fetching Data from API**:
   - The script makes a GET request to the API using the `requests` library in Python. The URL for the request is constructed dynamically using the `ROX_ENDPOINT` environment variable and a static part of the API path (`/v1/alerts?status=ACTIVE&namespace=*`).

3. **Handling JSON Data**:
   - The response from the API, expected in JSON format, is parsed to extract relevant alert data.

4. **Writing Data to a File**:
   - Extracted data is written to a file named `alerts.txt`. Each alert is converted to JSON format and stored as a separate line in this file.

5. **Converting JSON to CSV**:
   - To format the data in a more readable and standard format, we used `jq`, a command-line JSON processor, to convert the JSON data in `alerts.txt` into CSV format. This step is handled via a subprocess call in the script, which executes a `jq` command to perform the conversion and saves the result in `alerts.csv`.

### Script Execution Requirements
- **Environment Variables**: Before running the script, the `ROX_API_TOKEN` and `ROX_ENDPOINT` environment variables must be set with appropriate values.
- **Dependencies**: The script requires Python's `requests` library and the `jq` command-line tool installed on the system.
- **Security Note**: The script uses `verify=False` in the API request to bypass SSL certificate verification. This is generally not recommended for production environments due to security risks.

### Usage
Run the script in an environment where the required dependencies are installed, and the necessary environment variables are set. The script fetches the alert data, processes it, and generates a `alerts.csv` file with the formatted data.

`python report.py`
