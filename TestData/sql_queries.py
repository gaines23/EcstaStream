# DROP TABLES FIRST #

genre_table_drop = "DROP TABLE IF EXISTS app_genre;"
us_certs_table_drop = "DROP TABLE IF EXISTS app_uscerts;"
region_table_drop = "DROP TABLE IF EXISTS app_streamingregion;"
services_table_drop = "DROP TABLE IF EXISTS app_streamingservices;"




## (RE)CREATE TABLES ##
genre_table_create = ("""
    CREATE TABLE IF NOT EXISTS app_genre (
        id INT PRIMARY KEY
        , genre VARCHAR(50)
    )
""")

us_certs_table_create = ("""
    CREATE TABLE IF NOT EXISTS app_uscerts (
        us_certsID SERIAL PRIMARY KEY
        , certification VARCHAR(10)
        , meaning TEXT
    )
""")

region_table_create = ("""
    CREATE TABLE IF NOT EXISTS app_streamingregion (
        iso_3166_1 VARCHAR(5) PRIMARY KEY
        , native_name VARCHAR(20)
    )
""")

services_table_create = ("""
    CREATE TABLE IF NOT EXISTS app_streamingservices (
        provider_id INT PRIMARY KEY
        , display_priority INT
        , logo_path VARCHAR(200)
        , provider_name VARCHAR(150)
    )
""")





## INSERT DATA INTO TABLE ##

genre_table_insert = ("""
    INSERT INTO app_genre(id, genre)
    VALUES(%s, %s)
    ON CONFLICT(id)
    DO NOTHING
""")

streaming_services_table_insert = ("""
    INSERT INTO app_streamingservices(display_priority, logo_path, provider_name, provider_id)
    VALUES(%s, %s, %s, %s)
    ON CONFLICT(provider_id)
    DO NOTHING
""")

streaming_regions_table_insert = ("""
    INSERT INTO app_streamingregion(iso_3166_1, native_name)
    VALUES(%s, %s)
""")

us_certs_table_insert = ("""
    INSERT INTO app_uscerts(certification, meaning)
    VALUES(%s, %s)
""")


## create_tables.py commands

create_table_queries = [genre_table_create, us_certs_table_create, region_table_create, services_table_create]
drop_table_queries = [genre_table_drop, us_certs_table_drop, region_table_drop, services_table_drop]
insert_table_queries = [genre_table_insert, us_certs_table_insert, streaming_services_table_insert, streaming_regions_table_insert]

