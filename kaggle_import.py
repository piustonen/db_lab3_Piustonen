import csv
from datetime import date, datetime, timedelta
import random
from string import ascii_lowercase
import psycopg2

username = 'postgres'
password = '2010'
database = 'Piustonen01_DB'
host = 'localhost'
port = '5432'

# SELECT TRIM(genre_name) AS genre,
# COUNT(genre_id)
# FROM cloud_releases
# JOIN cloud_genres USING(genre_id)
# GROUP BY genre_name

# SELECT TRIM(artist_name) as artist,
# COUNT(song_id)
# FROM cloud_artists
# JOIN cloud_performances USING(artist_id)
# GROUP BY artist_name

# SELECT TRIM(genre_name) AS genre,
# COUNT(*) FROM cloud_performances
# JOIN cloud_songs USING(song_id)
# JOIN cloud_releases USING(song_id)
# JOIN cloud_genres USING(genre_id)
# WHERE perf_place != 'USA'
# GROUP BY genre_name


NAME = 'top 50 songs soundcloud 2022.csv'

conn = psycopg2.connect(user=username, password=password, dbname=database)


def get_date(start_date='2015-01-01', end_date='2019-12-31'):
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date


def get_perf_place():
    places = ['UK', 'France', 'Germany', 'USA', 'Italy']
    return random.choice(places)


def get_id(length, only_digits=False):
    list_of_chars = [str(i) for i in list(range(10))]
    if not only_digits:
        list_of_chars += ascii_lowercase
    return "".join(random.choices(list_of_chars, k=length))


with conn:
    cur = conn.cursor()

    # declare lists to store already existing rows to avoid 'duplicate key error' while inserting rows
    cur.execute("""SELECT * FROM cloud_genres;""")
    cloud_genres = [row[1].strip() for row in cur.fetchall()]

    cur.execute("""SELECT * FROM cloud_artists;""")
    cloud_artists = [row[1].strip() for row in cur.fetchall()]

    cur.execute("""SELECT * FROM cloud_songs;""")
    cloud_songs = [row[1].strip() for row in cur.fetchall()]

    cur.execute("""SELECT * FROM cloud_releases;""")
    releases_ids = [row[0].strip() for row in cur.fetchall()]

    cur.execute("""SELECT * FROM cloud_performances;""")
    performances_ids = [row[0].strip() for row in cur.fetchall()]

    genre_id = 10
    artist_id = 0
    song_id = 10

    with open(NAME, mode='r') as inf:
        reader = csv.DictReader(inf)
        for row in reader:
            artist_name = row['Artist.Name']
            song_genre = row['Genre']
            track_name = row['Track.Name']

            if song_genre not in cloud_genres:
                genre_id += 1
                cur.execute(f"""insert into cloud_genres (genre_id, genre_name) values (%s, %s)""",
                            [str(genre_id), song_genre])
                cloud_genres.append(song_genre)
            if artist_name not in cloud_artists:
                artist_id += 1
                cur.execute(f"""insert into cloud_artists (artist_id, artist_name) values (%s, %s)""",
                            [str(artist_id), artist_name])
                cloud_artists.append(artist_name)
            if track_name not in cloud_songs:
                song_id += 1
                cur.execute(f"""insert into cloud_songs (song_id, song_name) values (%s, %s)""",
                            [str(song_id), track_name])
                cloud_songs.append(track_name)

                release_id = get_id(length=4)
                release_date = get_date()
                while release_id in releases_ids:
                    release_id = get_id(length=4)
                cur.execute(
                    f"""insert into cloud_releases (release_id, genre_id, song_id, release_date) values (%s, %s, %s, %s)""",
                    [str(release_id), genre_id, song_id, release_date])
                releases_ids.append(release_id)

                performance_id = get_id(length=9, only_digits=True)
                performance_date = get_date(start_date=str(release_date))
                performance_place = get_perf_place()
                while performance_id in performances_ids:
                    performance_id = get_id(length=9, only_digits=True)
                cur.execute(
                    f"""insert into cloud_performances (perf_id, artist_id, song_id, perf_date, perf_place) values (%s, %s, %s, %s, %s)""",
                    [performance_id, artist_id, song_id, performance_date, performance_place])
                performances_ids.append(performance_id)

    conn.commit()
