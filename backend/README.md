# Mercury Python Backend

This folder contains the first Python/Postgres smoke test for Mercury.

## Setup

Create a virtual environment and install dependencies:

```powershell
cd C:\Users\grube\OneDrive\Documents\Mercury
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
```

Create `backend\.env` from `backend\.env.example` and update the connection string if your local Postgres user, password, database, or port differ.

```powershell
Copy-Item backend\.env.example backend\.env
```

## Read Clubs

```powershell
.\.venv\Scripts\python -m backend.read_clubs
```

The script reads the `clubs` table and prints each row in a compact terminal table.
