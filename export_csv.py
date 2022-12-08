import csv
import psycopg2

username = 'postgres'
password = '2010'
database = 'Piustonen01_DB'
host = 'localhost'
port = '5432'

output_file = 'export_csv_Piustonen_{}.csv'

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

    for table_name in TABLES:
        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]
        with open(output_file.format(table_name), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])
