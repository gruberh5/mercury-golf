from __future__ import annotations

from collections.abc import Iterable, Mapping

import psycopg

from backend.db import connect


CLUB_COLUMNS = (
    "club_id",
    "bag_id",
    "club_type",
    "manufacturer",
    "model",
    "loft",
    "shaft_model",
    "shaft_flex",
    "created_at",
)


def fetch_clubs() -> list[Mapping[str, object]]:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    club_id,
                    bag_id,
                    club_type,
                    manufacturer,
                    model,
                    loft,
                    shaft_model,
                    shaft_flex,
                    created_at
                FROM clubs
                ORDER BY club_id;
                """
            )
            return cur.fetchall()


def _format_value(value: object) -> str:
    return "" if value is None else str(value)


def _column_widths(rows: Iterable[Mapping[str, object]]) -> dict[str, int]:
    widths = {column: len(column) for column in CLUB_COLUMNS}

    for row in rows:
        for column in CLUB_COLUMNS:
            widths[column] = max(widths[column], len(_format_value(row[column])))

    return widths


def print_clubs(rows: list[Mapping[str, object]]) -> None:
    if not rows:
        print("Connected to Postgres. The clubs table exists, but it has no rows yet.")
        return

    widths = _column_widths(rows)
    header = " | ".join(column.ljust(widths[column]) for column in CLUB_COLUMNS)
    divider = "-+-".join("-" * widths[column] for column in CLUB_COLUMNS)

    print(header)
    print(divider)

    for row in rows:
        print(
            " | ".join(
                _format_value(row[column]).ljust(widths[column])
                for column in CLUB_COLUMNS
            )
        )


def main() -> None:
    try:
        rows = fetch_clubs()
    except psycopg.OperationalError as exc:
        raise SystemExit(
            "Could not connect to Postgres. Check backend\\.env and confirm the "
            "database is running.\n\n"
            f"Driver error: {exc}"
        ) from exc
    except psycopg.errors.UndefinedTable as exc:
        raise SystemExit(
            "Connected to Postgres, but the clubs table does not exist in this "
            "database. Run initial_schema.sql against the database in "
            "MERCURY_DATABASE_URL."
        ) from exc

    print_clubs(rows)


if __name__ == "__main__":
    main()
