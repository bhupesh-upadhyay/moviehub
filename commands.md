# login
psql -U moviehub
psql -U moviehub_user -d moviehub

# show DATABASES
\l

# Use DATABASE
\c moviehub

# Verify current database
SELECT current_database();

# show tables
\dt
\dt+

# upload
outside:
    mysql -u moviehub_user -p moviehub < data.sql
inside:
    \i data.sql

# exit
\q


MySQL                → PostgreSQL
-----------------------------------------
SHOW DATABASES;      → \l
USE db;              → \c db
SHOW TABLES;         → \dt
DESCRIBE table;      → \d table
IMPORT .sql          → psql -f file.sql
EXIT                 → \q

# truncate TABLES
TRUNCATE TABLE content_movie_genre, content_movie_actors, content_actor, content_genre, content_movie;

| Prompt | Meaning                             |
| ------ | ----------------------------------- |
| `=#`   | Ready for new command               |
| `-#`   | Waiting (no `;` yet)                |
| `'#`   | Inside string (missing closing `'`) |
| `(#`   | Unclosed parentheses                |

#Cancel current query:
\cancel
Ctrl + C

