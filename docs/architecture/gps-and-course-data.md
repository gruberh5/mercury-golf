# GPS And Course Data

GPS and course data are core to Mercury.

Mercury should eventually replace the on-course role of a premium GPS golf app, while also collecting data for analytics and AI caddie recommendations.

## Goals

- Show useful yardages during a round
- Identify the current hole
- Estimate distance to green and target points
- Support GPS imagery or mapped hole views
- Support a draggable target marker with dynamic yardage
- Capture shot start and end locations
- Estimate actual club distances
- Store enough location data to support post-round analysis

## On-Course Yardages

Mercury should support yardages to:

- Front green
- Middle green
- Back green
- Pin location when available
- Hazards
- Layup targets
- User-selected map targets

## Shot Tracking Concept

Early versions can use a manual GPS-assisted workflow:

1. User starts a shot
2. User selects club
3. Mercury records the current GPS position
4. User walks to the ball
5. User marks the result location
6. Mercury calculates estimated shot distance

This is not fully automatic shot detection, but it creates the foundation for Arccos-like insights.

## Course Data Needs

Mercury needs structured course information:

- Course name
- Hole number
- Par
- Tee locations
- Green locations
- Hazard locations
- Fairway and rough context
- Target points

## Preloaded Course Data

Course data should be loaded before the round whenever possible.

During active play, Mercury should avoid slow or expensive API calls. The app should use course data already stored in PostgreSQL, browser cache, or another local/offline-friendly layer.

Preloading should support:

- Course selection
- Tee selection
- Starting hole selection
- Hole maps
- Green coordinates
- Hazards
- Known layup targets
- User-created course notes

## API Research Questions

Before choosing a provider, Mercury needs to compare available golf course APIs and map data options.

Questions to answer:

- Which APIs provide course maps and green coordinates?
- Which APIs provide hazard locations?
- Which APIs allow mobile app usage?
- What are the costs and limits?
- Can course data be cached locally?
- Can user-created course data be stored in PostgreSQL?
- Can map imagery be used legally inside a personal app?
- What is the best map provider for mobile browser GPS use?
- Can we use API's for a "one time pull" of a course and its mapping, data, scorecard, etc. I do not play 25 unique courses a year its mostly repeats.

## Design Principle

Mercury should work even if a course API is imperfect.

The product should allow user-entered corrections and custom course notes over time.
