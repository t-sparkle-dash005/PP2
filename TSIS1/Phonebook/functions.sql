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