-- =====================================================
-- Mercury V2 Schema
-- Incorporates: course/tee/hole reference data (GolfCourseAPI + OSM),
-- fairway/GIR/putts tracking, and course-linked rounds.
-- =====================================================

-- -------------------------
-- Players
-- -------------------------

CREATE TABLE players (
    player_id BIGSERIAL PRIMARY KEY,

    name TEXT NOT NULL,
    handedness TEXT,
    age INTEGER,
    handicap NUMERIC(4,1),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Bags
-- -------------------------

CREATE TABLE bags (
    bag_id BIGSERIAL PRIMARY KEY,

    player_id BIGINT NOT NULL
        REFERENCES players(player_id),

    name TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT FALSE,

    golf_ball TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Clubs
-- -------------------------

CREATE TABLE clubs (
    club_id BIGSERIAL PRIMARY KEY,

    bag_id BIGINT NOT NULL
        REFERENCES bags(bag_id),

    club_type TEXT NOT NULL,

    manufacturer TEXT,
    model TEXT,

    loft NUMERIC(5,2),

    shaft_model TEXT,
    shaft_flex TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Courses
-- -------------------------
-- One row per physical golf course. Populated by importing
-- GolfCourseAPI data, then enriched with OSM green coordinates
-- when available.

CREATE TABLE courses (
    course_id BIGSERIAL PRIMARY KEY,

    golfcourseapi_id INTEGER,      -- external id from GolfCourseAPI, for re-syncing
    club_name TEXT,
    course_name TEXT NOT NULL,

    city TEXT,
    state TEXT,
    country TEXT,
    address TEXT,

    has_osm_mapping BOOLEAN NOT NULL DEFAULT FALSE,  -- did we find usable OSM green/hole data?

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Holes
-- -------------------------
-- One row per hole per course. Par and hole_number typically come
-- from OSM's golf=hole ref/par tags when available, falling back to
-- GolfCourseAPI's per-tee hole array position/par otherwise.
-- green_lat/green_lon are NULL when no OSM mapping exists for this
-- course -- in that case Mercury falls back to a live on-course tap
-- to get a yardage instead of a stored coordinate.

CREATE TABLE holes (
    hole_id BIGSERIAL PRIMARY KEY,

    course_id BIGINT NOT NULL
        REFERENCES courses(course_id),

    hole_number INTEGER NOT NULL,
    par INTEGER NOT NULL,

    green_lat NUMERIC(10,8),
    green_lon NUMERIC(11,8),

    UNIQUE (course_id, hole_number)
);

-- -------------------------
-- Tees
-- -------------------------
-- One row per tee set per course (Blue, White, Gold, etc.),
-- split by gender the way GolfCourseAPI provides it.

CREATE TABLE tees (
    tee_id BIGSERIAL PRIMARY KEY,

    course_id BIGINT NOT NULL
        REFERENCES courses(course_id),

    tee_name TEXT NOT NULL,
    gender TEXT NOT NULL,          -- 'male' or 'female', as provided by GolfCourseAPI

    course_rating NUMERIC(4,1),
    slope_rating INTEGER,
    total_yards INTEGER,
    par_total INTEGER
);

-- -------------------------
-- Tee Holes (join table)
-- -------------------------
-- Yardage and stroke index are properties of a hole *as played from
-- a specific tee*, not of the hole itself -- they vary by tee set.

CREATE TABLE tee_holes (
    tee_id BIGINT NOT NULL
        REFERENCES tees(tee_id),

    hole_id BIGINT NOT NULL
        REFERENCES holes(hole_id),

    yardage INTEGER NOT NULL,
    handicap_index INTEGER NOT NULL,   -- stroke index for this hole from this tee

    PRIMARY KEY (tee_id, hole_id)
);

-- -------------------------
-- Rounds
-- -------------------------

CREATE TABLE rounds (
    round_id BIGSERIAL PRIMARY KEY,

    player_id BIGINT NOT NULL
        REFERENCES players(player_id),

    bag_id BIGINT NOT NULL
        REFERENCES bags(bag_id),

    tee_id BIGINT NOT NULL
        REFERENCES tees(tee_id),       -- course + tee set both derive from this

    played_at TIMESTAMP NOT NULL,
    course_handicap INTEGER,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Hole Scores
-- -------------------------

CREATE TABLE hole_scores (
    hole_score_id BIGSERIAL PRIMARY KEY,

    round_id BIGINT NOT NULL
        REFERENCES rounds(round_id),

    hole_id BIGINT NOT NULL
        REFERENCES holes(hole_id),     -- par is looked up via this, not stored redundantly

    score INTEGER NOT NULL,
    putts INTEGER NOT NULL,

    fairway_result TEXT,   -- 'hit', 'left', 'right', 'short', 'long', NULL for par 3s
    green_result   TEXT,   -- 'hit', 'left', 'right', 'short', 'long'

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Shots
-- -------------------------

CREATE TABLE shots (
    shot_id BIGSERIAL PRIMARY KEY,

    round_id BIGINT NOT NULL
        REFERENCES rounds(round_id),

    hole_id BIGINT NOT NULL
        REFERENCES holes(hole_id),

    club_id BIGINT NOT NULL
        REFERENCES clubs(club_id),

    start_lat NUMERIC(10,8),
    start_lon NUMERIC(11,8),

    end_lat NUMERIC(10,8),
    end_lon NUMERIC(11,8),

    shot_timestamp TIMESTAMP NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Recommendations
-- -------------------------

CREATE TABLE recommendations (
    recommendation_id BIGSERIAL PRIMARY KEY,

    shot_id BIGINT NOT NULL
        REFERENCES shots(shot_id),

    recommended_club TEXT,
    recommended_target TEXT,

    reason TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
