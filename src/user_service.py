# Copyright 2020 N26 GmbH

from typing import Set
from utils import read_csv_file


def read_active_users(filename: str) -> Set[str]:
    """Read users.csv and return a set of active user IDs."""
    active_users = set()
    for row in read_csv_file(filename):
        if row['is_active'] == '1':
            active_users.add(row['user_id'])
    return active_users 