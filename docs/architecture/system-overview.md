# System Overview

Mercury should be designed as a layered system.

## Layers

### 1. Data Layer

Stores structured information about rounds, shots, equipment, courses, weather, recommendations, and outcomes.

Planned database: PostgreSQL.

### 2. GPS And Course Data Layer

Handles the on-course location and map context.

Examples:

- Current GPS position
- Course
- Current hole
- Green locations
- Hazards
- Target points
- Shot start and end locations
- Yardages to targets

### 3. Domain Layer

Defines the golf concepts Mercury understands.

Examples:

- Player profile
- Equipment profile
- Shot
- Lie
- Target
- Risk
- Recommendation
- Decision outcome

### 4. AI Caddie And Recommendation Layer

Produces on-course decision support.

Early versions can use rules, player profile data, bag setup, and known tendencies. Later versions can use deeper statistical modeling and historical outcomes. Later versions could also recommend and assist me in preparation for rounds in terms of what clubs are best to hit off the tee. Not sure what else could be gained from forecasting besides tee shot forecasting.

The caddie should recommend:

- Club
- Target
- Risk level
- Reason
- Alternative option when useful

### 5. Analytics Layer

Produces post-round and long-term insights.

Examples:

- Club performance
- Equipment comparison
- Miss patterns
- Decision risk analysis
- Scoring trends
- Strokes gained analysis
- R visualizations

R is expected to become part of the analytics workflow later.

### 6. Interface Layer

Provides the user experience.

Long-term target: mobile-first Progressive Web App.

## Modes

### On-Course Mode

Fast, minimal, and focused.

Primary output:

- GPS yardage
- Current hole and score
- Shot tracking controls
- Club recommendation
- Target recommendation
- Risk level
- Short explanation

### Analysis Mode

Detailed and reflective. All on PC, not mobile.

Primary output:

- Trends
- Comparisons
- Round reviews
- Equipment analysis
- Decision analysis
- Strokes gained analysis
- Visualizations

## Recommended Build Order

1. Documentation
2. Data model
3. Mobile-first GPS scorecard prototype
4. Basic course and hole data
5. GPS-assisted shot tracking
6. PostgreSQL storage
7. Simple AI caddie prototype
8. Post-round analytics
9. R analytics and visualization
10. Weather and richer course data integrations
