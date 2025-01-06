
\c diplom_db;

create schema if not exists dip_schema;

SET search_path to dip_schema;

CREATE TABLE IF NOT EXISTS press_release (
    id SERIAL PRIMARY KEY,
    text TEXT NULL,
    key_rate NUMERIC,
    source_text VARCHAR(255), -- link to cbr materials
    release_date timestamp
);