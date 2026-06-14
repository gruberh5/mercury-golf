-- =====================================================
-- Mercury V1 Initial Schema
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
-- Rounds
-- -------------------------

CREATE TABLE rounds (
    round_id BIGSERIAL PRIMARY KEY,

    player_id BIGINT NOT NULL
        REFERENCES players(player_id),

    bag_id BIGINT NOT NULL
        REFERENCES bags(bag_id),

    played_at TIMESTAMP NOT NULL,

    course_name TEXT,
    tee_name TEXT,

    slope INTEGER,
    rating NUMERIC(4,1),

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

    hole_number INTEGER NOT NULL,

    score INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- Shots
-- -------------------------

CREATE TABLE shots (
    shot_id BIGSERIAL PRIMARY KEY,

    round_id BIGINT NOT NULL
        REFERENCES rounds(round_id),

    club_id BIGINT NOT NULL
        REFERENCES clubs(club_id),

    hole_number INTEGER NOT NULL,

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