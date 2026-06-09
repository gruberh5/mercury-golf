# R Analytics Plan

R is a future analytics layer for Mercury.

The app does not need to start with R, but the data model should preserve the information needed for R analysis later.

## Purpose

Use R for deeper analysis, visualizations, and statistical review of personal golf performance.

## Possible Analyses

- Strokes gained matrix
- Club distance distributions
- Shot dispersion charts
- Miss tendency by club
- Lie impact analysis
- Equipment comparisons
- Driver vs mini driver scoring impact
- Ball performance comparison
- Aggressive vs conservative target outcomes
- Round trend visualizations

## Data Needed

- Round
- Hole
- Shot number
- Club
- Equipment setup
- Ball
- Start location
- End location
- Start distance to hole
- End distance to hole
- Start lie
- End lie
- Penalties
- Intended target
- Actual outcome
- Recommendation shown
- Decision quality
- Execution quality
- Outcome quality

## Early R Workflow

Early R work can happen outside the app:

1. Export data from PostgreSQL (can't we just sync the two?)
2. Analyze in R
3. Create charts and summaries
4. Use findings to improve Mercury recommendations

## Long-Term R Workflow

Later, Mercury may run scheduled analytics jobs and store summary results back into PostgreSQL for the app to display.
