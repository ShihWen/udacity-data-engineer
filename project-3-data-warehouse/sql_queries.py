import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events
(
  artist        varchar(256),
  auth          varchar(99),
  firstName     varchar(99),
  gender        varchar(3),
  itemInSession integer,
  lastName      varchar(99),
  length        DECIMAL(10,5),
  level         varchar(10),
  location      varchar(99),
  method        varchar(10),
  page          varchar(20),
  registration  varchar(20),
  sessionId     varchar(20),
  song          varchar(256),
  status        varchar(10),
  ts            BIGINT,
  userAgent     varchar(256),
  userId        integer
  
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs
(
    artist_id        varchar(99) NOT NULL,
    artist_latitude  DECIMAL(10,5)     ,
    artist_location  varchar(256) ,
    artist_longitude DECIMAL(10,5)     ,
    artist_name      varchar(256) ,
    duration         DECIMAL(10,5)     ,
    num_songs        integer     ,
    song_id          varchar(99) ,
    title            varchar(256) ,
    year             integer     
)
""")

songplay_table_create = ("""
CREATE TABLE songplays
(
    songplay_id integer     identity(0,1),
    start_time  datetime     ,
    user_id     integer     ,
    level       varchar(256) ,
    song_id     varchar(256) ,
    artist_id   varchar(256) ,
    session_id  varchar(256) ,
    location    varchar(256) ,
    user_agent  varchar(256) 
)
""")

user_table_create = ("""
CREATE TABLE users
(
    user_id    integer     ,
    first_name varchar(256) ,
    last_name  varchar(256) ,
    gender     varchar(256)  ,
    level      varchar(256) 
)
""")

song_table_create = ("""
CREATE TABLE songs
(
    song_id   varchar(256) ,
    title     varchar(256) ,
    artist_id varchar(256) ,
    year      integer     ,
    duration  DECIMAL(10,5)  
)
""")

artist_table_create = ("""
CREATE TABLE artists
(
    artist_id  varchar(256) ,
    name       varchar(256) ,
    location   varchar(256) ,
    latitude   DECIMAL(10,5)     ,
    longitude  DECIMAL(10,5)    
)
""")

time_table_create = ("""
CREATE TABLE time 
(
    start_time datetime NOT NULL,
    hour       integer NOT NULL,
    day        integer NOT NULL,
    week       integer NOT NULL,
    month      integer NOT NULL,
    year       integer NOT NULL,
    weekday    integer NOT NULL
)
""")

# STAGING TABLES
# https://knowledge.udacity.com/questions/625921
LOG_DATA     = config.get("S3", "LOG_DATA")
ARN          = config.get("IAM_ROLE", "ARN")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")      
SONG_DATA    = config.get("S3", "SONG_DATA")


staging_events_copy = ("""
    copy staging_events 
    from {}
    credentials 'aws_iam_role={}' 
    json {}
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs 
    from {} 
    credentials 'aws_iam_role={}' 
    json 'auto';
""").format(SONG_DATA, ARN)


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays
(
	--songplay_id, 
	start_time,
	user_id,
	artist_id,
	session_id,
	location,
	user_agent,
    song_id,
    level
)
SELECT  TIMESTAMP 'epoch'+(ts/1000)*INTERVAL '1 second'
	,A.userId
	,B.artist_id
	,A.sessionId
	,A.location
	,A.userAgent
    ,B.song_id
    ,A.level
FROM staging_events A
INNER JOIN staging_songs B
ON A.artist = B.artist_name
AND A.song = B.title
AND A.length = B.duration
WHERE A.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users
(user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId
	        ,firstName
		,lastName
		,gender
		,level
FROM staging_events
""")

song_table_insert = ("""
INSERT INTO songs
(song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id
		,title
		,artist_id
		,year
		,duration
FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id
		,artist_name
		,artist_location
		,artist_latitude
		,artist_longitude
FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time
(start_time, hour, day, week, month, year, weekday)
SELECT  DISTINCT start_time
	,EXTRACT(HOUR FROM start_time)
	,EXTRACT(DAY FROM start_time)
	,DATE_PART(w, start_time)
	,EXTRACT( MONTH FROM start_time)
	,EXTRACT( YEAR FROM start_time)
	,DATE_PART(dow, start_time)
FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
