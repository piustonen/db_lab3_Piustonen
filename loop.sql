SELECT * FROM cloud_releases;
CREATE TABLE relcopy AS SELECT * FROM cloud_releases;
SELECT * FROM relcopy;
DELETE FROM relcopy;

 DO $$
 DECLARE 
 	rel_id relcopy.release_id%TYPE;
 	gen_id relcopy.genre_id%TYPE;
 	s_id relcopy.song_id%TYPE;
	
 BEGIN
 	rel_id   := '2000';
 	gen_id   := '100';
 	s_id     := '0';
 	FOR counter IN 1..9
 		LOOP
 			INSERT INTO relcopy(release_id, genre_id, song_id, release_date)
 			VALUES (rel_id || counter, 
					gen_id || counter, 
					s_id || counter, 
					(SELECT CURRENT_DATE));
 		END LOOP;
 END;
 $$
