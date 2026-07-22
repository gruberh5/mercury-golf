# MVP Scope

The MVP should prove that Mercury can support an actual round of golf while capturing useful personal data.

The first version should include GPS yardage and score tracking because those are central to the product identity. I should be able to load up this app on the first teebox and be confident in its ability to work all round long.

The first version does not need to perfectly match every premium app feature. It should prove the basic on-course workflow and create a foundation for the AI caddie and analytics system.

## MVP Goals

* Capture round and shot data manually
* Show GPS-based yardages during a round
* Track score and basic stats
* Log shot start and end locations when possible
* Estimate actual club distances from GPS points
* Track equipment used during each round
* Track basic shot outcomes and miss patterns
* Track club performance over time
* Compare equipment setups
* Produce post-round analytics
* Prototype AI caddie recommendations

## In Scope

* Round logging
* Hole-by-hole scoring
* Mobile-first on-course interface
* Start-round flow for choosing course, tees, starting hole, equipment setup, and ball
* Preloaded or cached course data for active play
* GPS location capture
* Distance to green or selected target
* Draggable map target with dynamic yardage
* Basic course and hole data
* Shot notes
* Shot start location
* Shot end location
* Club used
* Estimated shot distance
* Intended target
* Actual result
* Miss direction
* Lie type
* Penalty tracking
* Equipment setup tracking
* Basic club performance summaries
* Basic decision outcome review
* Simple caddie recommendation with explanation
* Data storage in PostgreSQL once the database phase begins

## Out Of Scope For MVP

* App Store distribution
* Fully automatic Arccos-style shot detection
* Perfect course mapping for every course
* Advanced strokes-gained modeling
* Production R analytics workflows
* Machine learning models
* Paid or commercial API commitments before research

## MVP Questions To Answer

* Where are strokes being lost?
* Are GPS-derived shot distances matching expected club distances?
* Which clubs create the most trouble?
* Which clubs create the most confidence?
* Is mini driver outperforming driver?
* Which equipment setup produces better scoring?
* Are aggressive targets helping or hurting?
* Do certain lies change shot outcomes?
* What recommendation would Mercury make in a real on-course situation?

## MVP Success Criteria

The MVP is successful if it can be used during a real round for yardages, scoring, basic shot tracking, and at least one useful recommendation or post-round insight.

## Suggested MVP Phases

### Phase 1: Playable GPS Scorecard

* Mobile-first round screen
* Start-round flow
* Preloaded course and tee selection
* Current hole
* GPS yardage
* Hole map or satellite imagery concept
* Draggable target marker
* Score entry
* Basic stats

### Phase 2: GPS-Assisted Shot Tracking

* Mark shot start
* Mark shot result
* Store club used
* Calculate estimated shot distance

### Phase 3: Personal Caddie Prototype

* Enter lie, wind, pin, hazard, and confidence (is this too much entry? hazard should be able to be inferred by caddie thru GPS.)
* Receive club and target recommendation
* Store recommendation and actual outcome

### Phase 4: Post-Round Analytics

* Club distance summaries
* Miss patterns
* Equipment comparisons
* Decision review



### Phase 4 / 5 (Future): Multi-User / Player Profiles / Recommendation Input



Not in scope for the current build. Revisit only after Mercury is proven

solo, for real, across multiple rounds.



* Real authentication (signup/login), replacing the single shared

&#x20; password gate used for solo/private testing. 

* Player-facing profile creation: name, bag setup, etc. (schema already

&#x20; supports this via the existing players/bags tables -- this is a UI +

&#x20; auth gap, not a data model gap). 

* A "describe your golf game" input of some kind, feeding the future

&#x20; recommendation engine -- exact shape (skill self-assessment? shot

&#x20; tendencies? something else?) still undesigned, needs its own

&#x20; dedicated design pass, not a quick bolt-on. 

* Per-player data scoping across all API endpoints once real accounts

&#x20; exist.


## Elevation-Adjusted Yardage (Phase 1, not deferred)

Since elevation data is free (Mapbox Terrain-RGB, covered under the
standard tile free tier) and a hole's elevation profile is fixed
(doesn't change round to round, unlike wind), this is being built
alongside the core GPS-yardage feature, not pushed to a later phase.

- Pull elevation at player's live position and at the green.
- Apply a slope-adjustment formula (rule-of-thumb: ~1 effective yard
  per yard of elevation change, refine later if needed) to show a
  "plays like" distance alongside the raw straight-line yardage.

## Wind-Adjusted Yardage (Future phase, genuinely deferred)

Unlike elevation, wind is a live, constantly-changing variable
requiring real-time weather data and directional math relative to the
shot line. Meaningfully harder problem than elevation -- treat as a
separate, later phase once the AI caddie concept is being built out for
real, not bundled with elevation.

