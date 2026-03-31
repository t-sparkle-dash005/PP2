CREATE OR REPLACE PROCEDURE upsert_student(
    p_name VARCHAR,
    p_phone VARCHAR,
    p_faculty VARCHAR DEFAULT 'General'
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM students WHERE student_name = p_name) THEN
        UPDATE students
        SET student_phone = p_phone,
            student_faculty = p_faculty
        WHERE student_name = p_name;
    ELSE
        INSERT INTO students(student_name, student_phone, student_faculty)
        VALUES (p_name, p_phone, p_faculty);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_upsert_students(
    p_records TEXT[],
    OUT p_invalid_records TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    v_rec TEXT;
    v_name TEXT;
    v_phone TEXT;
    v_faculty TEXT;
    v_split TEXT[];
BEGIN
    p_invalid_records := ARRAY[]::TEXT[];
    FOREACH v_rec IN ARRAY p_records LOOP
        v_split := string_to_array(v_rec, '|');
        IF array_length(v_split, 1) != 3 THEN
            p_invalid_records := array_append(p_invalid_records, v_rec || ' (bad format)');
            CONTINUE;
        END IF;

        v_name := trim(v_split[1]);
        v_phone := trim(v_split[2]);
        v_faculty := trim(v_split[3]);

        IF v_name = '' OR v_phone = '' OR v_faculty = '' THEN
            p_invalid_records := array_append(p_invalid_records, v_rec || ' (missing fields)');
            CONTINUE;
        END IF;

        IF v_phone !~ '^\\+?[0-9\- ]{7,20}$' THEN
            p_invalid_records := array_append(p_invalid_records, v_rec || ' (invalid phone)');
            CONTINUE;
        END IF;

        CALL upsert_student(v_name, v_phone, v_faculty);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_student(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Either name or phone must be provided';
    END IF;

    DELETE FROM students
    WHERE (p_name IS NOT NULL AND student_name = p_name)
       OR (p_phone IS NOT NULL AND student_phone = p_phone);
END;
$$;
