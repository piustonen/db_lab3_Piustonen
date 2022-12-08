import json
import psycopg2

username = 'postgres'
password = '2010'
database = 'Piustonen01_DB'
host = 'localhost'
port = '5432'
output_file = {}

TABLES = [
    'cloud_genres',
    'cloud_songs',
    'cloud_artists',
    'cloud_releases',
    'cloud_performances',
]

conn = psycopg2.connect(user=username, password=password, dbname=database)


with conn:
    cur = conn.cursor()

    for table in TABLES:
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]
        for row in cur:
            rows.append(dict(zip(fields, row)))
        output_file[table] = rows
with open('export_json.json', 'w') as outf:
    json.dump(output_file, outf, default=str)
