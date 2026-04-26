-- ── 1. Groups / categories ───────────────────────────────────
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed default categories
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;


-- ── 2. Core contacts table ────────────────────────────────────
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(50)  UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ  DEFAULT NOW()
);

-- Migrate: add new columns to an existing table without breaking it
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email      VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday   DATE,
    ADD COLUMN IF NOT EXISTS group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- Remove the old single-phone column only if it still exists
-- (Practice 8 stored phone directly on contacts; phones are now in phones table)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'contacts' AND column_name = 'phone'
    ) THEN
        ALTER TABLE contacts DROP COLUMN phone;
    END IF;
END;
$$;


-- ── 3. Phones table (1-to-many) ───────────────────────────────
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER     NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) NOT NULL DEFAULT 'mobile'
    CHECK (type IN ('home', 'work', 'mobile'))
);