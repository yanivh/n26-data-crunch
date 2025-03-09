# Copyright 2020 N26 GmbH

import csv
import os
from typing import List, Any


def read_csv_file(filename: str) -> List[dict]:
    """Read any CSV file and return list of dictionaries."""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_data(out: str, header: List[str], data: List[List[Any]]) -> bool:
    """Write data to CSV file."""
    if os.path.exists(out):
        print('File %s already exists!' % out)
        return False

    try:
        with open(out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
    except Exception as err:
        print('Failed to write %s' % out)
        return False
    return True 