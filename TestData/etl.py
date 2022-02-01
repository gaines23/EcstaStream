from sql_queries import *

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
    genre_data = df[['id', 'name']].drop_duplicates()

    for i, row in genre_data.iterrows():
        cur.execute(genre_table_insert, row)


def process_providers_file(cur, filepath):
    providers_files = get_files("data/provider/provider")
    filepath = providers_files[0]
    df = pd.read_json(filepath, lines=True)

    provider_data = df[['display_priority', 'logo_path', 'provider_name', 'provider_id']].drop_duplicates()

    for i, row in provider_data.iterrows():
        cur.execute(streaming_providers_insert, row)


def process_provider_regions_file(cur, filepath):
    region_files = get_files("data/provider/region")
    filepath = region_files[0]
    df = pd.read_json(filepath, lines=True)

    region_data = df[['iso_3166_1', 'native_name']].drop_duplicates()

    for i, row in region_data.iterrows():
        cur.execute(streaming_regions_insert, row)



def process_data(cur, conn, filepath, func):

    """
    The function below processes the data based on the cur, conn, filepath, and func
    commands defined above. process_data reads and abstracts the information in the
    files in the defined filepaths and iterates through the process until there 
    is no more data to read over.  
    """

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
    conn = psycopg2.connect("host=127.0.0.1 dbname=StreamingApp user=postgres password=Nala$2323")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/genre', func=process_genre_file)
    process_data(cur, conn, filepath='data/provider/provider', func=process_providers_file)
    process_data(cur, conn, filepath='data/provider/region', func=process_provider_regions_file)

    conn.close()


if __name__ == "__main__":
    main()