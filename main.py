import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

username = 'postgres'
password = '2010'
database = 'Piustonen01_DB'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW QuantityGenre AS
SELECT TRIM(genre_name) AS genre, 
COUNT(genre_id) 
FROM cloud_releases 
JOIN cloud_genres USING(genre_id) 
GROUP BY genre_name
'''

query_2 = '''
CREATE VIEW ArtistCount AS
SELECT TRIM(artist_name) as artist, 
COUNT(song_id) 
FROM cloud_artists 
JOIN cloud_performances USING(artist_id) 
GROUP BY artist_name
'''

query_3 = '''
CREATE VIEW QuantityNOTUSA AS
SELECT TRIM(genre_name) AS genre, 
COUNT(*) FROM cloud_performances 
JOIN cloud_songs USING(song_id) 
JOIN cloud_releases USING(song_id) 
JOIN cloud_genres USING(genre_id) 
WHERE perf_place != 'USA' 
GROUP BY genre_name
'''

conn = psycopg2.connect(user = username, password = password, dbname = database, host = host, port = port)

with conn:
    print("Database opened successfully")
    cur = conn.cursor()

    cur.execute('Drop view if exists QuantityGenre')
    print('1.\n')
    cur.execute(query_1)
    cur.execute('SELECT * FROM QuantityGenre')

    periods = []
    p_count = []
    plt.xticks(rotation=10)
    for row in cur:
        periods.append(row[0])
        p_count.append(row[1])
    sns.barplot(x = periods , y = p_count)
    plt.show()


    print('2.\n')
    cur.execute('Drop view if exists ArtistCount')
    cur.execute(query_2)
    cur.execute('SELECT * FROM ArtistCount')
    periods = []
    p_count = []
    for row in cur:
        periods.append(row[0])
        p_count.append(row[1])
    fig1, ax1 = plt.subplots()
    ax1.pie(p_count,  labels=periods, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()


    print('3.\n')
    cur.execute('Drop view if exists QuantityNOTUSA')

    cur.execute(query_3)
    cur.execute('SELECT * FROM QuantityNOTUSA')
    periods = []
    p_count = []
    plt.xticks(rotation=10)
    for row in cur:
        periods.append(row[0])
        p_count.append(row[1])
    sns.lineplot(x = periods, y = p_count)
    plt.show()
