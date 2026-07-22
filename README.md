# Mercury

Mercury is a personal golf intelligence platform.

The goal is to build a personal version of a premium golf GPS, scoring, stat tracking, shot tracking, analytics, and AI caddie platform.

Mercury should replace the need for apps like 18Birdies during a round while becoming more personalized than a generic golf app can be. It should combine GPS yardages, course information, player tendencies, equipment data, weather, historical performance, and golf strategy into real-time recommendations and post-round analytics.

Mercury informs decisions. Mercury does not make decisions.

## Current Stage

Mercury is in product and architecture design.

No application code has been started yet. The current focus is defining:

- Product vision
- Core principles
- MVP scope
- System architecture
- Data model
- Player and equipment profiles
- GPS, course data, and AI caddie design
- R analytics plan

## Documentation

Start here:

- [Product Vision](docs/product/vision.md)
- [Product Principles](docs/product/principles.md)
- [MVP Scope](docs/product/mvp-scope.md)
- [App Flow](docs/product/app-flow.md)
- [System Overview](docs/architecture/system-overview.md)
- [Initial Data Model](docs/architecture/data-model.md)
- [GPS And Course Data](docs/architecture/gps-and-course-data.md)
- [AI Caddie Design](docs/architecture/ai-caddie.md)
- [R Analytics Plan](docs/analytics/r-analytics-plan.md)
- [Player Profile](docs/golf-domain/player-profile.md) - current source of truth for player tendencies, equipment, ball, and carry distances
- [Equipment Profile](docs/golf-domain/equipment-profile.md) - how Mercury should evaluate equipment over time
- [Game Profile Input Guide](docs/golf-domain/game-profile-input.md) - optional guide for what to add to the player profile

## Long-Term Direction

Mercury is intended to become a mobile-first web application that can be added to an iPhone home screen as a Progressive Web App.

The long-term target is a self-built premium golf app with:

- GPS yardages
- Score and stat tracking
- GPS-assisted shot distance tracking
- Equipment tracking
- Post-round analytics
- R-based analysis and visualization
- AI caddie recommendations during the round

The first useful version should prove the on-course workflow: GPS yardage, score tracking, basic shot logging, and a simple AI caddie prototype.

## Local Prototype

The first frontend prototype lives in `frontend/`.

To run it locally:

```powershell
cd C:\Users\grube\OneDrive\Documents\Mercury\frontend
npm run dev
```

Then open:

```text
http://127.0.0.1:5173/
```

## Python/Postgres Smoke Test

The first Python backend smoke test lives in `backend/`.

To connect Python to your local Postgres database and read the `clubs` table:

```powershell
cd C:\Users\grube\OneDrive\Documents\Mercury
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
.\.venv\Scripts\python -m backend.read_clubs
```

Edit `backend\.env` if your local Postgres connection is not:

```text
postgresql://postgres:postgres@localhost:5432/mercury
```
