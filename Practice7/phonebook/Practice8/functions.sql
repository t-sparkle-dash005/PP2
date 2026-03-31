CREATE OR REPLACE FUNCTION get_students_by_pattern(p_pattern TEXT)
RETURNS TABLE(
    student_id INTEGER,
    student_name VARCHAR,
    student_phone VARCHAR,
    student_faculty VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT student_id, student_name, student_phone, student_faculty
    FROM students
    WHERE student_name ILIKE '%' || p_pattern || '%'
       OR student_phone ILIKE '%' || p_pattern || '%'
       OR student_faculty ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_students_paginated(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(
    student_id INTEGER,
    student_name VARCHAR,
    student_phone VARCHAR,
    student_faculty VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT student_id, student_name, student_phone, student_faculty
    FROM students
    ORDER BY student_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
