CREATE OR REPLACE FUNCTION delete_old_row() RETURNS TRIGGER AS $delete_old_row$
    DECLARE
        full_count integer;
        max_count integer;
    BEGIN
        max_count := TG_ARGV[0];

        EXECUTE format('SELECT Count(id) FROM %I.%I', TG_TABLE_SCHEMA, TG_TABLE_NAME) INTO STRICT full_count;
        IF full_count > max_count THEN
            EXECUTE format('DELETE FROM %I.%I ' ||
                   'WHERE created = ' ||
                        '(SELECT Min(created) FROM %I.%I)',
                    TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_TABLE_SCHEMA, TG_TABLE_NAME);
        END IF;
        RETURN NULL;
    END;
$delete_old_row$ LANGUAGE plpgsql;
