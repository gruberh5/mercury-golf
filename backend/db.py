from __future__ import annotations

import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


ENV_FILE = Path(__file__).with_name(".env")


def _load_local_env() -> None:
    if not ENV_FILE.exists():
        return

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_database_url() -> str:
    _load_local_env()

    database_url = os.getenv("MERCURY_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "Set MERCURY_DATABASE_URL in backend\\.env or in your shell environment."
        )

    return database_url


def connect() -> psycopg.Connection:
    return psycopg.connect(get_database_url(), row_factory=dict_row)
