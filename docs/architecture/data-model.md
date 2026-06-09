# Initial Data Model

This document defines the first version of Mercury's data model.

It is not a final database schema yet. It is a plain-English map of the things Mercury needs to track.

## Core Entities

### Player Profile

Information about the player and current tendencies.

Examples:

- Driver tendencies
- Iron tendencies
- Wedge tendencies
- Putting confidence
- Shot shape
- Common misses

### Equipment Item

A single piece of equipment.

Examples:

- Driver
- Mini driver
- 7 wood
- 4 iron
- Putter
- Golf ball

### Equipment Setup

A group of equipment used during a round.

Example:

- Driver A
- Mini driver
- Iron set
- Wedges
- Putter
- Ball A

### Course

The golf course.

Examples:

- Course name
- Location
- Tees played
- Source of course data
- Course map metadata

### Hole

A hole on a course.

Examples:

- Hole number
- Par
- Yardage
- Hazards
- Green shape
- Front green coordinate
- Middle green coordinate
- Back green coordinate
- Known target points

### Round

A single round of golf.

Examples:

- Date
- Course
- Tee
- Score
- Equipment setup
- Weather summary
- Starting handicap or index context if useful

### Shot

One shot during a round.

Examples:

- Hole
- Shot number
- Club
- Distance
- Start GPS coordinate
- End GPS coordinate
- Lie
- Intended target
- Result
- Miss direction
- Penalty
- Shot shape
- Contact quality
- Confidence before shot

### Decision Context

The situation before a shot.

This may become the most important part of Mercury.

Examples:

- Distance to target
- Distance to front green
- Distance to middle green
- Distance to back green
- Pin position
- Wind
- Elevation
- Lie type
- Hazards
- Confidence
- Score situation
- Available clubs
- Ball being played
- Equipment setup

### Recommendation

What Mercury suggested.

Examples:

- Recommended club
- Recommended target
- Risk level
- Explanation
- Alternative club or target
- Confidence level
- Data used for the recommendation

### Decision Outcome

What happened after the decision.

Examples:

- Was the decision conservative, neutral, or aggressive?
- Did the shot match the intended target?
- Was the miss acceptable?
- Did the decision cost or save strokes?

### GPS Position

A location point captured during a round.

Examples:

- Latitude
- Longitude
- Timestamp
- Accuracy estimate
- Round
- Hole
- Related shot if applicable

### Course Feature

A mapped feature on a course.

Examples:

- Green
- Bunker
- Water
- Out of bounds
- Fairway
- Tee box
- Layup target

### Strokes Gained Observation

A future analytics entity for comparing shot outcomes to expected scoring baselines.

Examples:

- Starting distance
- Starting lie
- Ending distance
- Ending lie
- Penalty
- Expected strokes before
- Expected strokes after
- Strokes gained value

## Important Design Rule

Mercury should not treat result quality as the same thing as decision quality.

A shot can have:

- Good decision, good execution, good outcome
- Good decision, bad execution, bad outcome
- Good decision, bad execution, lucky outcome
- Bad decision, good execution, lucky outcome
- Bad decision, bad execution, bad outcome

This distinction should influence the database design later.
