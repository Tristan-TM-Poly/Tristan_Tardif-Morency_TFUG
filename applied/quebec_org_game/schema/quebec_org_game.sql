-- Quebec Organizations Exploration Game
-- Coupled parallel schema for organizations, events, evidence, scoring, gameplay, and governance.

CREATE TABLE organizations (
  org_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  org_type TEXT NOT NULL,
  sector TEXT,
  headquarters_region TEXT,
  ownership_type TEXT,
  website TEXT,
  wikidata_id TEXT,
  created_at TEXT,
  updated_at TEXT
);

CREATE TABLE relationships (
  rel_id TEXT PRIMARY KEY,
  source_org_id TEXT NOT NULL,
  target_org_id TEXT NOT NULL,
  rel_type TEXT NOT NULL,
  start_date TEXT,
  end_date TEXT,
  confidence REAL,
  notes TEXT
);

CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL,
  event_title TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_date TEXT,
  jurisdiction TEXT,
  summary TEXT NOT NULL,
  status TEXT,
  impact_direction TEXT,
  severity INTEGER,
  confidence REAL,
  created_at TEXT,
  updated_at TEXT
);

CREATE TABLE dimensions (
  dimension_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE event_dimension_scores (
  eds_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  dimension_id TEXT NOT NULL,
  score REAL NOT NULL,
  rationale TEXT,
  confidence REAL
);

CREATE TABLE sources (
  source_id TEXT PRIMARY KEY,
  source_type TEXT NOT NULL,
  title TEXT NOT NULL,
  publisher TEXT,
  url TEXT,
  publication_date TEXT,
  jurisdiction TEXT,
  reliability_tier INTEGER,
  archived_url TEXT
);

CREATE TABLE event_sources (
  event_source_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  source_id TEXT NOT NULL,
  quote TEXT,
  source_claim_type TEXT,
  supports_which_part TEXT
);

CREATE TABLE claims (
  claim_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  claim_text TEXT NOT NULL,
  claim_polarity TEXT,
  claim_status TEXT,
  confidence REAL
);

CREATE TABLE outcomes (
  outcome_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  outcome_type TEXT NOT NULL,
  amount REAL,
  amount_currency TEXT,
  outcome_date TEXT,
  notes TEXT
);

CREATE TABLE gameplay_profiles (
  profile_id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL,
  environment_score REAL,
  labour_score REAL,
  transparency_score REAL,
  public_value_score REAL,
  tax_fairness_score REAL,
  competition_score REAL,
  privacy_score REAL,
  indigenous_relations_score REAL,
  regional_development_score REAL,
  safety_score REAL,
  scientific_integrity_score REAL,
  total_score REAL,
  profile_state TEXT,
  updated_at TEXT
);

CREATE TABLE quests (
  quest_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  quest_type TEXT NOT NULL,
  region TEXT,
  sector TEXT,
  objective TEXT NOT NULL,
  difficulty INTEGER,
  reward_type TEXT,
  created_at TEXT
);

CREATE TABLE quest_targets (
  quest_target_id TEXT PRIMARY KEY,
  quest_id TEXT NOT NULL,
  org_id TEXT,
  event_id TEXT,
  source_id TEXT,
  target_role TEXT
);

CREATE TABLE governance_flags (
  flag_id TEXT PRIMARY KEY,
  org_id TEXT,
  event_id TEXT,
  profile_id TEXT,
  flag_type TEXT NOT NULL,
  flag_status TEXT NOT NULL,
  rationale TEXT,
  confidence REAL,
  created_at TEXT
);

CREATE TABLE data_ingestion_runs (
  run_id TEXT PRIMARY KEY,
  source_system TEXT NOT NULL,
  scope TEXT,
  started_at TEXT,
  finished_at TEXT,
  status TEXT,
  records_seen INTEGER,
  records_created INTEGER,
  records_updated INTEGER,
  notes TEXT
);

CREATE INDEX idx_events_org_id ON events(org_id);
CREATE INDEX idx_relationships_source ON relationships(source_org_id);
CREATE INDEX idx_relationships_target ON relationships(target_org_id);
CREATE INDEX idx_event_sources_event_id ON event_sources(event_id);
CREATE INDEX idx_event_sources_source_id ON event_sources(source_id);
CREATE INDEX idx_claims_event_id ON claims(event_id);
CREATE INDEX idx_outcomes_event_id ON outcomes(event_id);
CREATE INDEX idx_gameplay_profiles_org_id ON gameplay_profiles(org_id);
CREATE INDEX idx_governance_flags_org_id ON governance_flags(org_id);
CREATE INDEX idx_governance_flags_event_id ON governance_flags(event_id);
