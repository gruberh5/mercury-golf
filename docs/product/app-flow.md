# App Flow

This document describes the main product flow for Mercury.

The app should feel like a personal premium golf GPS, scorecard, shot tracker, and AI caddie.

## Primary App Modes

Mercury will likely need several main areas:

- Play
- Courses
- Rounds
- Player Profile
- Analytics

The first build should focus on Play.

## Before A Round

Before reaching the first tee, the user needs to start a round.

The start-round flow should include:

- Choose course
- Choose tees
- Choose starting hole
- Choose equipment setup
- Confirm golf ball
- Confirm round date and time
- Load pre-cached course data

## Course Data Principle

Courses should be preloaded before the round whenever possible.

Mercury should avoid slow or expensive API calls during active play. During a round, the app should mostly use locally stored or database-cached course data.

APIs can still be used for course discovery, imports, updates, or preparation before the round.

## First Tee Screen

When standing on the tee box, the first screen should show GPS imagery of the current hole.

The hole view should include:

- Current hole map or satellite imagery
- Current GPS position
- Tee location
- Green location
- Hazards when known
- A draggable target marker
- Dynamic yardage from current position to the target marker
- Basic hole information
- Score entry access
- Shot tracking controls
- Caddie button

## Draggable Yardage Marker

The draggable marker is a core interaction.

The user should be able to touch or drag a target point on the hole map and immediately see yardage to that point.

This supports:

- Carry distance to hazards
- Layup decisions
- Target selection
- Approach planning
- AI caddie context

## AI Caddie Interaction

The caddie should be available from the hole map screen.

The interaction should feel like a dialogue box or popover, not a separate complicated screen.

The caddie popup should show:

- Recommended club
- Recommended target
- Risk level
- Short explanation
- Safer option if useful
- Aggressive option if useful

The user should be able to close the caddie and return immediately to the hole map.

## During The Hole

The active-hole workflow should support:

- Start shot
- Select club
- Store shot start GPS position
- Walk to ball
- Mark shot result
- Store shot end GPS position
- Calculate estimated shot distance
- Continue to next shot
- Enter score and stats

## After The Round

After the round, Mercury should support:

- Score summary
- Shot review
- Club distance review
- Miss pattern review
- Equipment setup review
- Caddie recommendation review
- Notes for future rounds

## Open Product Questions

- What should the home screen show when no round is active?
- Should the app open directly into Play mode if a round is active?
- How should course search and course prep work?
- How much profile editing should happen inside the app versus in documentation at first?
- Should analytics be a separate tab or part of round history?
- What is the simplest useful version of the hole map?
