

genre_table_insert = ("""
    INSERT INTO app_genre(id, genre)
    VALUES(%s, %s)
    ON CONFLICT(id)
    DO NOTHING
""")

providers_table_insert = ("""
    INSERT INTO app_providers(display_priority, logo_path, provider_name, provider_id)
    VALUES(%s, %s, %s, %s)
""")