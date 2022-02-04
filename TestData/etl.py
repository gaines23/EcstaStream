from sql_queries import *
import configparser

import os
import glob
import psycopg2
import pandas as pd



def get_files(filepath):
    """
        This query below defines the get_files command used to find
        and extract and store information into the correct SQL tables
        defined in the sql_queries.py file.
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files


def process_genre_file(cur, filepath):
    # open genre file
    genre_files = get_files("data/genre")
    filepath = genre_files[0]
    df = pd.read_json(filepath, lines=True)

    # insert genre record
    genre_data = df[['id', 'genre']].drop_duplicates()

    for i, row in genre_data.iterrows():
        cur.execute(genre_table_insert, row)

def process_services_file(cur, filepath):
    services_files = get_files("data/streaming/services")
    filepath = services_files[0]
    df = pd.read_json(filepath, lines=True)

    services_data = df[['display_priority', 'logo_path', 'provider_name', 'provider_id']].drop_duplicates()

    for i, row in services_data.iterrows():
        cur.execute(streaming_services_table_insert, row)

def process_provider_regions_file(cur, filepath):
    region_files = get_files("data/streaming/region")
    filepath = region_files[0]
    df = pd.read_json(filepath, lines=True)

    region_data = df[['iso_3166_1', 'native_name']].drop_duplicates()

    for i, row in region_data.iterrows():
        cur.execute(streaming_regions_table_insert, row)

def process_us_certs_file(cur, filepath):
    certs_files = get_files("data/certs")
    filepath = certs_files[0]
    df = pd.read_json(filepath, lines=True)

    certs_data = df[['certification', 'meaning']].drop_duplicates()

    for i, row in certs_data.iterrows():
        cur.execute(us_certs_table_insert, row)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    config = configparser.ConfigParser()
    config.read('ecst.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/genre', func=process_genre_file)
    process_data(cur, conn, filepath='data/streaming/services', func=process_services_file)
    process_data(cur, conn, filepath='data/streaming/region', func=process_provider_regions_file)
    process_data(cur, conn, filepath='data/certs', func=process_us_certs_file)

    conn.close()


if __name__ == "__main__":
    main()