-- =========================
-- GENRES (20)
-- =========================
INSERT INTO content_genre (id, name) VALUES
(1,'Action'),(2,'Comedy'),(3,'Drama'),(4,'Sci-Fi'),(5,'Thriller'),
(6,'Horror'),(7,'Romance'),(8,'Adventure'),(9,'Fantasy'),(10,'Mystery'),
(11,'Crime'),(12,'Animation'),(13,'Family'),(14,'War'),(15,'History'),
(16,'Music'),(17,'Sport'),(18,'Biography'),(19,'Documentary'),(20,'Western');

-- =========================
-- ACTORS (20)
-- =========================
INSERT INTO content_actor (id, name, birth_date) VALUES
(1,'Leonardo DiCaprio','1974-11-11'),
(2,'Scarlett Johansson','1984-11-22'),
(3,'Robert Downey Jr.','1965-04-04'),
(4,'Tom Holland','1996-06-01'),
(5,'Morgan Freeman','1937-06-01'),
(6,'Brad Pitt','1963-12-18'),
(7,'Angelina Jolie','1975-06-04'),
(8,'Johnny Depp','1963-06-09'),
(9,'Tom Cruise','1962-07-03'),
(10,'Keanu Reeves','1964-09-02'),
(11,'Chris Evans','1981-06-13'),
(12,'Emma Watson','1990-04-15'),
(13,'Will Smith','1968-09-25'),
(14,'Natalie Portman','1981-06-09'),
(15,'Hugh Jackman','1968-10-12'),
(16,'Dwayne Johnson','1972-05-02'),
(17,'Jennifer Lawrence','1990-08-15'),
(18,'Chris Hemsworth','1983-08-11'),
(19,'Gal Gadot','1985-04-30'),
(20,'Henry Cavill','1983-05-05');

-- =========================
-- MOVIES (20)
-- =========================
INSERT INTO content_movie
(id,title,description,release_year,duration,thumbnail,video_url,created_at)
VALUES
(1,'Inception','Dream within dreams',2010,8880,'thumbnails/inception.jpg','https://ex.com/1',CURRENT_TIMESTAMP),
(2,'Avengers','Superhero battle',2012,9000,'thumbnails/avengers.jpg','https://ex.com/2',CURRENT_TIMESTAMP),
(3,'Interstellar','Space exploration',2014,10140,'thumbnails/interstellar.jpg','https://ex.com/3',CURRENT_TIMESTAMP),
(4,'Titanic','Love story on ship',1997,11700,'thumbnails/titanic.jpg','https://ex.com/4',CURRENT_TIMESTAMP),
(5,'Joker','Origin of Joker',2019,7320,'thumbnails/joker.jpg','https://ex.com/5',CURRENT_TIMESTAMP),
(6,'Matrix','Virtual reality world',1999,8160,'thumbnails/matrix.jpg','https://ex.com/6',CURRENT_TIMESTAMP),
(7,'Gladiator','Roman warrior story',2000,9300,'thumbnails/gladiator.jpg','https://ex.com/7',CURRENT_TIMESTAMP),
(8,'Avatar','Alien planet story',2009,9720,'thumbnails/avatar.jpg','https://ex.com/8',CURRENT_TIMESTAMP),
(9,'Batman','Dark knight rises',2008,9120,'thumbnails/batman.jpg','https://ex.com/9',CURRENT_TIMESTAMP),
(10,'Iron Man','Tech superhero',2008,7560,'thumbnails/ironman.jpg','https://ex.com/10',CURRENT_TIMESTAMP),
(11,'Thor','God of thunder',2011,7800,'thumbnails/thor.jpg','https://ex.com/11',CURRENT_TIMESTAMP),
(12,'Hulk','Green giant hero',2003,8400,'thumbnails/hulk.jpg','https://ex.com/12',CURRENT_TIMESTAMP),
(13,'Deadpool','Funny antihero',2016,6480,'thumbnails/deadpool.jpg','https://ex.com/13',CURRENT_TIMESTAMP),
(14,'Spiderman','Teen superhero',2017,7200,'thumbnails/spiderman.jpg','https://ex.com/14',CURRENT_TIMESTAMP),
(15,'Doctor Strange','Magic hero',2016,6900,'thumbnails/strange.jpg','https://ex.com/15',CURRENT_TIMESTAMP),
(16,'Black Panther','Wakanda king',2018,8040,'thumbnails/panther.jpg','https://ex.com/16',CURRENT_TIMESTAMP),
(17,'Captain America','Super soldier',2011,7440,'thumbnails/cap.jpg','https://ex.com/17',CURRENT_TIMESTAMP),
(18,'Wonder Woman','Amazon warrior',2017,8520,'thumbnails/ww.jpg','https://ex.com/18',CURRENT_TIMESTAMP),
(19,'Superman','Man of steel',2013,8580,'thumbnails/superman.jpg','https://ex.com/19',CURRENT_TIMESTAMP),
(20,'Fast & Furious','Street racing',2001,6360,'thumbnails/ff.jpg','https://ex.com/20',CURRENT_TIMESTAMP);

-- =========================
-- MOVIE-GENRE RELATION
-- =========================
INSERT INTO content_movie_genres (id,movie_id,genre_id) VALUES
(1,1,4),(2,1,5),
(3,2,1),(4,2,8),
(5,3,4),(6,3,3),
(7,4,7),(8,4,3),
(9,5,3),(10,5,11),
(11,6,4),(12,6,1),
(13,7,14),(14,7,3),
(15,8,9),(16,8,8),
(17,9,1),(18,9,5),
(19,10,1),(20,10,4),
(21,11,9),(22,11,1),
(23,12,1),(24,12,4),
(25,13,2),(26,13,1),
(27,14,1),(28,14,8),
(29,15,9),(30,15,4),
(31,16,1),(32,16,8),
(33,17,14),(34,17,1),
(35,18,9),(36,18,1),
(37,19,4),(38,19,1),
(39,20,1),(40,20,17);

-- =========================
-- MOVIE-ACTOR RELATION
-- =========================
INSERT INTO content_movie_actors (id,movie_id,actor_id) VALUES
(1,1,1),(2,2,3),(3,3,1),(4,4,1),(5,5,6),
(6,6,10),(7,7,6),(8,8,16),(9,9,11),(10,10,3),
(11,11,18),(12,12,13),(13,13,15),(14,14,4),(15,15,14),
(16,16,19),(17,17,11),(18,18,19),(19,19,20),(20,20,16);