-- CorridorIQ Pipeline Supabase Schema
-- This extends the existing schema from supabase/migrations/001_schema.sql
-- with raw data ingestion tables for the pipeline.
--
-- The processed tables (ports, corridors, corridor_scores) are already
-- defined in 001_schema.sql. This file adds the raw ingestion tier.

-- =============================================================================
-- RAW TIER: ingestion tables for source data
-- =============================================================================

CREATE TABLE IF NOT EXISTS raw_oecd_emissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ref_area TEXT NOT NULL,
    country_name TEXT,
    vessel TEXT,
    vessel_emissions_source TEXT,
    time_period TEXT,
    emissions_tonnes_co2 DOUBLE PRECISION,
    methodology TEXT,
    ingested_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw_wpi_ports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    wpi_index_number TEXT UNIQUE,
    port_name TEXT NOT NULL,
    country TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    harbor_size TEXT,
    harbor_type TEXT,
    shelter_afforded TEXT,
    cargo_pier_depth_m DOUBLE PRECISION,
    channel_depth_m DOUBLE PRECISION,
    has_electricity BOOLEAN DEFAULT false,
    has_rail BOOLEAN DEFAULT false,
    has_fuel_oil BOOLEAN DEFAULT false,
    has_diesel BOOLEAN DEFAULT false,
    repairs TEXT,
    dry_dock TEXT,
    railway TEXT,
    ingested_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS on raw tables
ALTER TABLE raw_oecd_emissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_wpi_ports ENABLE ROW LEVEL SECURITY;

-- Service role can read/write; anon has no access to raw data
CREATE POLICY "Service role access on raw_oecd_emissions"
    ON raw_oecd_emissions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role access on raw_wpi_ports"
    ON raw_wpi_ports FOR ALL USING (auth.role() = 'service_role');
