#!/usr/bin/env python3
"""
crt.sh Query Tool
Query certificate transparency logs for a specific domain.
"""

import argparse
import json
import sys
import csv
from datetime import datetime
from typing import List, Dict, Any
import urllib.request
import urllib.parse
import urllib.error


def query_crtsh(domain: str, wildcard: bool = False, exclude_expired: bool = False) -> List[Dict[str, Any]]:
    """
    Query crt.sh for certificate information.

    Args:
        domain: Domain name to query
        wildcard: If True, prepend % to domain for wildcard search
        exclude_expired: If True, exclude expired certificates

    Returns:
        List of certificate records
    """
    query_domain = f"%.{domain}" if wildcard else domain

    params = {
        'q': query_domain,
        'output': 'json'
    }

    if exclude_expired:
        params['exclude'] = 'expired'

    url = f"https://crt.sh/?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"Error querying crt.sh: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def format_text(records: List[Dict[str, Any]]) -> str:
    """Format records as human-readable text."""
    if not records:
        return "No certificates found."

    output = []
    output.append(f"Found {len(records)} certificate(s)\n")
    output.append("=" * 80)

    for i, record in enumerate(records, 1):
        output.append(f"\nCertificate #{i}")
        output.append("-" * 80)
        output.append(f"  Domain(s):        {record.get('name_value', 'N/A')}")
        output.append(f"  Issuer:           {record.get('issuer_name', 'N/A')}")
        output.append(f"  Not Before:       {record.get('not_before', 'N/A')}")
        output.append(f"  Not After:        {record.get('not_after', 'N/A')}")
        output.append(f"  Certificate ID:   {record.get('id', 'N/A')}")
        output.append(f"  Logged At:        {record.get('entry_timestamp', 'N/A')}")
        output.append(f"  Serial Number:    {record.get('serial_number', 'N/A')}")

    return "\n".join(output)


def format_csv(records: List[Dict[str, Any]]) -> str:
    """Format records as CSV."""
    if not records:
        return "id,name_value,issuer_name,not_before,not_after,entry_timestamp,serial_number\n"

    output = []

    # CSV header
    fieldnames = ['id', 'name_value', 'issuer_name', 'not_before', 'not_after', 'entry_timestamp', 'serial_number']

    # Use StringIO to write CSV in memory
    import io
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()

    for record in records:
        # Replace newlines in name_value for CSV compatibility
        if 'name_value' in record:
            record['name_value'] = record['name_value'].replace('\n', '; ')
        writer.writerow(record)

    return csv_buffer.getvalue()


def format_json(records: List[Dict[str, Any]]) -> str:
    """Format records as JSON."""
    return json.dumps(records, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Query crt.sh for certificate transparency logs',
        epilog='Example: %(prog)s -d example.com -o output.txt -f text'
    )

    parser.add_argument(
        '-d', '--domain',
        required=True,
        help='Domain name to query'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (if not specified, prints to stdout)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['text', 'csv', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '-w', '--wildcard',
        action='store_true',
        help='Use wildcard search (prepends %% to domain)'
    )

    parser.add_argument(
        '-e', '--exclude-expired',
        action='store_true',
        help='Exclude expired certificates'
    )

    args = parser.parse_args()

    # Query crt.sh
    print(f"Querying crt.sh for domain: {args.domain}", file=sys.stderr)
    records = query_crtsh(args.domain, args.wildcard, args.exclude_expired)
    print(f"Retrieved {len(records)} records", file=sys.stderr)

    # Format output
    if args.format == 'text':
        output = format_text(records)
    elif args.format == 'csv':
        output = format_csv(records)
    elif args.format == 'json':
        output = format_json(records)
    else:
        print(f"Unknown format: {args.format}", file=sys.stderr)
        sys.exit(1)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Output written to: {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == '__main__':
    main()
