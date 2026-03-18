PRAGMA foreign_keys = OFF;

DELETE FROM content_movie_actors;
DELETE FROM content_movie_genres;
DELETE FROM content_movie;
DELETE FROM content_actor;
DELETE FROM content_genre;

DELETE FROM sqlite_sequence WHERE name IN (
'content_movie',
'content_actor',
'content_genre',
'content_movie_actors',
'content_movie_genres'
);

PRAGMA foreign_keys = ON;