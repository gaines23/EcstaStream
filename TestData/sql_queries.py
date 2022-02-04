# DROP TABLES FIRST #

genre_table_drop = "DROP TABLE IF EXISTS app_genre"
certs_table_drop = "DROP TABLE IF EXISTS app_certs"
countries_table_drop = "DROP TABLE IF EXISTS app_countries"
region_table_drop = "DROP TABLE IF EXISTS app_regions"
services_table_drop = "DROP TABLE IF EXISTS app_services"


genre_table_create = ("""
    CREATE TABLE IF NOT EXISTS app_genre (
        id INT PRIMARY KEY
        , genre TEXT []
    )
""")

certs_table_create = (""""
    CREATE TABLE IF NOT EXISTS app_certs (
        certifications 
    )
""")

genre_table_insert = ("""
    INSERT INTO app_genre(id, genre)
    VALUES(%s, %s)
    ON CONFLICT(id)
    DO NOTHING
""")

streaming_providers_insert = ("""
    INSERT INTO app_streamingproviders(display_priority, logo_path, provider_name, provider_id)
    VALUES(%s, %s, %s, %s)
    ON CONFLICT(provider_id)
    DO NOTHING
""")

streaming_regions_insert = ("""
    INSERT INTO app_streamingregion(iso_3166_1, native_name)
    VALUES(%s, %s)
""")
