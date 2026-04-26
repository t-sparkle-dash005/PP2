-- ============================================================
-- procedures.sql  –  All PL/pgSQL server-side objects (TSIS1)
-- Includes everything from Practice 8 + new objects for TSIS1.
-- ============================================================

-- Drop old Practice 8 signature (3-param) if it still exists
DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR, VARCHAR);


-- ─────────────────────────────────────────────────────────────
-- PROCEDURE: upsert_contact
-- Insert a contact; update first_name / email / birthday /
-- group_id if the username already exists.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username   VARCHAR,
    p_first_name VARCHAR,
    p_email      VARCHAR  DEFAULT NULL,
    p_birthday   DATE     DEFAULT NULL,
    p_group_id   INTEGER  DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO contacts (username, first_name, email, birthday, group_id)
    VALUES (p_username, p_first_name, p_email, p_birthday, p_group_id)
    ON CONFLICT (username)
    DO UPDATE SET
        first_name = EXCLUDED.first_name,
        email      = COALESCE(EXCLUDED.email,     contacts.email),
        birthday   = COALESCE(EXCLUDED.birthday,  contacts.birthday),
        group_id   = COALESCE(EXCLUDED.group_id,  contacts.group_id);
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- FUNCTION: bulk_insert_contacts
-- Insert many contacts at once.
-- Validates phone format; returns array of bad rows.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION bulk_insert_contacts(
    p_usernames   VARCHAR[],
    p_first_names VARCHAR[],
    p_phones      VARCHAR[],
    p_types       VARCHAR[]           -- phone type per row
)
RETURNS TEXT[]
LANGUAGE plpgsql AS $$
DECLARE
    i             INT;
    v_phone       VARCHAR;
    v_type        VARCHAR;
    v_contact_id  INT;
    v_invalid     TEXT[];
BEGIN
    v_invalid := ARRAY[]::TEXT[];

    FOR i IN 1 .. array_length(p_usernames, 1) LOOP
        v_phone := p_phones[i];
        v_type  := COALESCE(p_types[i], 'mobile');

        -- Validate phone: 7-20 chars, only digits / + - ( ) space
        IF v_phone ~ '^[0-9\+\-\(\) ]{7,20}$' THEN

            -- Upsert the contact row (no phone column on contacts any more)
            INSERT INTO contacts (username, first_name)
            VALUES (p_usernames[i], p_first_names[i])
            ON CONFLICT (username)
            DO UPDATE SET first_name = EXCLUDED.first_name
            RETURNING id INTO v_contact_id;

            -- If INSERT returned nothing it was an UPDATE; fetch the id
            IF v_contact_id IS NULL THEN
                SELECT id INTO v_contact_id
                FROM contacts WHERE username = p_usernames[i];
            END IF;

            -- Add the phone (avoid exact duplicate on same contact)
            INSERT INTO phones (contact_id, phone, type)
            VALUES (v_contact_id, v_phone, v_type)
            ON CONFLICT DO NOTHING;

        ELSE
            v_invalid := array_append(
                v_invalid,
                p_usernames[i] || ' – invalid phone: ' || v_phone
            );
        END IF;
    END LOOP;

    RETURN v_invalid;
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- PROCEDURE: delete_contact
-- Delete by username or phone.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE PROCEDURE delete_contact(
    p_identifier VARCHAR,
    p_type       VARCHAR   -- 'username' | 'phone'
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_type = 'username' THEN
        DELETE FROM contacts WHERE username = p_identifier;
    ELSIF p_type = 'phone' THEN
        DELETE FROM contacts
        WHERE id IN (
            SELECT contact_id FROM phones WHERE phone = p_identifier
        );
    ELSE
        RAISE EXCEPTION 'p_type must be "username" or "phone", got: %', p_type;
    END IF;
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- PROCEDURE: add_phone  (NEW – TSIS1)
-- Add a phone number to an existing contact by username.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- Look up the contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- Validate type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home / work / mobile, got: %', p_type;
    END IF;

    -- Validate phone format
    IF NOT (p_phone ~ '^[0-9\+\-\(\) ]{7,20}$') THEN
        RAISE EXCEPTION 'Invalid phone number: %', p_phone;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- PROCEDURE: move_to_group  (NEW – TSIS1)
-- Move a contact to a group; create the group if it doesn't exist.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id   INT;
    v_contact_id INT;
BEGIN
    -- Ensure the contact exists
    SELECT id INTO v_contact_id
    FROM contacts WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- Get or create the group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- FUNCTION: search_contacts  (EXTENDED – TSIS1)
-- Pattern-match against username, first_name, email, AND
-- every phone number stored in the phones table.
-- Returns one row per contact (uses DISTINCT ON to de-duplicate).
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INT,
    username   VARCHAR,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.id)
           c.id,
           c.username,
           c.first_name,
           c.email,
           c.birthday,
           g.name  AS group_name
    FROM   contacts c
    LEFT JOIN groups g  ON g.id = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE  c.username   ILIKE '%' || p_query || '%'
       OR  c.first_name ILIKE '%' || p_query || '%'
       OR  c.email      ILIKE '%' || p_query || '%'
       OR  ph.phone     ILIKE '%' || p_query || '%'
    ORDER BY c.id;
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- FUNCTION: get_contacts_page  (Practice 8, kept / updated)
-- Paginated listing with optional sort column.
-- sort_by: 'name' | 'birthday' | 'created_at'  (default: 'name')
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION get_contacts_page(
    page_num  INT,
    page_size INT,
    sort_by   VARCHAR DEFAULT 'name'
)
RETURNS TABLE (
    id         INT,
    username   VARCHAR,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id,
           c.username,
           c.first_name,
           c.email,
           c.birthday,
           g.name AS group_name
    FROM   contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY
        CASE WHEN sort_by = 'birthday'   THEN c.birthday::TEXT   END ASC NULLS LAST,
        CASE WHEN sort_by = 'created_at' THEN c.created_at::TEXT END ASC NULLS LAST,
        CASE WHEN sort_by = 'name'
               OR sort_by NOT IN ('birthday', 'created_at')
             THEN c.first_name END ASC
    LIMIT  page_size
    OFFSET (page_num - 1) * page_size;
END;
$$;


-- ─────────────────────────────────────────────────────────────
-- FUNCTION: filter_by_group  (NEW – TSIS1)
-- Return every contact belonging to a named group.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION filter_by_group(p_group_name VARCHAR)
RETURNS TABLE (
    id         INT,
    username   VARCHAR,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.first_name, c.email, c.birthday
    FROM   contacts c
    JOIN   groups   g ON g.id = c.group_id
    WHERE  g.name ILIKE p_group_name;
END;
$$;