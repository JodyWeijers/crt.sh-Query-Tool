# crt.sh Query Tool

A command-line tool for querying certificate transparency logs from crt.sh. This script allows you to search for SSL/TLS certificates associated with a specific domain and export the results in multiple formats.

## Overview

Certificate Transparency (CT) is an internet security standard for monitoring and auditing the issuance of digital certificates. This tool queries the crt.sh database to retrieve certificate information for any given domain.

## Features

- Query certificate transparency logs for any domain
- Multiple output formats: text, CSV, and JSON
- Wildcard search support for subdomain discovery
- Filter expired certificates
- Save results to file or output to stdout
- Detailed certificate information including issuer, validity dates, and serial numbers

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Clone this repository or download the script:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Make the script executable:

```bash
chmod +x crtsh_query.py
```

## Usage

### Basic Syntax

```bash
./crtsh_query.py -d DOMAIN [OPTIONS]
```

### Command-Line Options

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-h` | `--help` | Show help message and exit |
| `-d DOMAIN` | `--domain DOMAIN` | Domain name to query (required) |
| `-o OUTPUT` | `--output OUTPUT` | Output file path (optional, prints to stdout if not specified) |
| `-f FORMAT` | `--format FORMAT` | Output format: text, csv, or json (default: text) |
| `-w` | `--wildcard` | Use wildcard search to include subdomains |
| `-e` | `--exclude-expired` | Exclude expired certificates from results |

## Examples

### Basic Query

Query certificates for a domain and display results as text:

```bash
./crtsh_query.py -d example.com
```

### JSON Output to File

Save results in JSON format:

```bash
./crtsh_query.py -d example.com -f json -o example_certs.json
```

### CSV Output to File

Save results in CSV format for use in spreadsheets:

```bash
./crtsh_query.py -d example.com -f csv -o example_certs.csv
```

### Wildcard Search

Search for all subdomains using wildcard (prepends % to domain):

```bash
./crtsh_query.py -d example.com -w
```

### Exclude Expired Certificates

Filter out expired certificates from results:

```bash
./crtsh_query.py -d example.com -e
```

### Combined Options

Search for all subdomains, exclude expired certificates, and save as JSON:

```bash
./crtsh_query.py -d example.com -w -e -f json -o active_certs.json
```

## Output Formats

### Text Format

Human-readable format with detailed certificate information:

```
Found 100 certificate(s)

================================================================================

Certificate #1
--------------------------------------------------------------------------------
  Domain(s):        example.com
  Issuer:           C=US, O=Let's Encrypt, CN=R3
  Not Before:       2024-01-01T00:00:00
  Not After:        2024-04-01T00:00:00
  Certificate ID:   12345678
  Logged At:        2024-01-01T00:01:00.000
  Serial Number:    abc123...
```

### CSV Format

Comma-separated values suitable for spreadsheet applications:

```csv
id,name_value,issuer_name,not_before,not_after,entry_timestamp,serial_number
12345678,example.com,"C=US, O=Let's Encrypt, CN=R3",2024-01-01T00:00:00,2024-04-01T00:00:00,2024-01-01T00:01:00.000,abc123...
```

### JSON Format

Machine-readable JSON array of certificate objects:

```json
[
  {
    "id": 12345678,
    "name_value": "example.com",
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "not_before": "2024-01-01T00:00:00",
    "not_after": "2024-04-01T00:00:00",
    "entry_timestamp": "2024-01-01T00:01:00.000",
    "serial_number": "abc123..."
  }
]
```

## Certificate Fields

The tool retrieves the following information for each certificate:

- **id**: Certificate ID in the crt.sh database
- **name_value**: Domain name(s) covered by the certificate
- **issuer_name**: Certificate issuer information
- **not_before**: Certificate validity start date
- **not_after**: Certificate validity end date
- **entry_timestamp**: When the certificate was logged
- **serial_number**: Certificate serial number

## Use Cases

- Security auditing and monitoring
- Subdomain enumeration
- Certificate inventory management
- Tracking certificate issuance history
- Identifying misconfigured or unauthorized certificates
- Research and reconnaissance

## How It Works

The script queries the crt.sh API using HTTPS requests. The crt.sh service aggregates certificate data from Certificate Transparency logs maintained by various certificate authorities and organizations.

When you perform a query:

1. The script constructs a URL with appropriate parameters
2. Sends an HTTPS request to crt.sh
3. Receives JSON data containing certificate records
4. Formats the data according to your specified output format
5. Either displays the results or saves them to a file

## Error Handling

The script includes error handling for common issues:

- Network connectivity problems
- Invalid domain names
- API timeout errors
- File write permissions
- Malformed JSON responses

Error messages are printed to stderr while keeping stdout clean for piping output.

## Limitations

- Query results depend on what has been logged in Certificate Transparency logs
- Very popular domains may return thousands of results
- The crt.sh service may occasionally be slow or unavailable
- Rate limiting may apply for excessive queries

## License

This project is provided as-is for educational and security research purposes.

## Disclaimer

This tool is intended for legitimate security research, auditing, and monitoring purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations.

## Resources

- crt.sh website: https://crt.sh
- Certificate Transparency RFC: https://tools.ietf.org/html/rfc6962
- Certificate Transparency specification: https://certificate.transparency.dev

## Version History

- 1.0.0 - Initial release with text, CSV, and JSON output formats
