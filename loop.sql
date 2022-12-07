DO $$
 DECLARE
     genres_id   genres.genre_id%TYPE;
     genres_name genres.genre_name%TYPE;

 BEGIN
     genres_id := 'ID';
     genres_name := 'GenreName';
     FOR counter IN 1..20
         LOOP
            INSERT INTO Genres (genre_id, genre_name)
             VALUES (genres_id || counter, genres_name || counter);
         END LOOP;
 END;
 $$
