# Udacity Data Engineer Project 1: Data Modeling with Postgres


  1. The purpose of the database in the context of the startup, Sparkify, and their analytical goals.
      - To provide profiles of Sparkify users in terms of their memeber status, location, the devices they're using , which songs they are listening to and the time they play the song.
      - In short, understanding who(user status), where(location), when(play time), what(what songs) and how (what device).
      - The analytical goals is to understanding their members first, and improve their service from those understandings.
  <br>

  2. How to run the Python scripts <br>
  Run it in a terminal tab with command:
      ```
      python [your_python_file_name].py
      ```
  3. An explanation of the files in the repository
      -  `Data` : Where all raw data files are kept, includes both log files and song files.
      - `sql_queries.py`: SQL queries for all queries that will be executed in other files during the ETL process, includes `create_tables.py` and `etl.py`.
      - `cretate_tables.py`: Consist of 4 functions.
        - `create_database()` for creating database `sprkifydb` and return connection and cursor variables for other functions to use.
        - `drop_tables(cur, conn)` for dropping tables if existing.
        - `create_tables(cur, conn)` for creating new empty tables.
        - `main()` for combining previous 3 functions and close connection when done.
      - `etl.py`: Consist of 4 functions.
        - `process_song_file(cur, filepath)` for processing song files using `pandas`for 2 related tables first, namely `songs` table and `artist` table. Then insert into tables. The insert queries used here are imported from `sql_queries.py`.
        - `process_log_file(cur, filepath)` for processing log files using `pandas`for 3 related tables first, namely `time` table, `users` table and `songplays` table. Then insert into tables. The insert queries used here are imported from `sql_queries.py`.
        - `process_data(cur, conn, filepath, func)` gets all the files from given path and count the total number, then iterate through those files with given function while printing out the current process status at the terminal.
        - `main()` combines all previous steps into one: Connect to the database, create curser, process song data and insert data into related tables, process log data and insert data into related tables, and close connection.
      - `etl.ipynb`: Same logic as `etl.py` but break down into smaller steps with explanations.
      - `test.ipynb` for checking if the data is inserted successfully after running `etl.py` or `etl.ipynb`.
  <br>
  
  4. Dataset and Database Schema
      - Song dataset
        ```
        {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
        ```
      - Log dataset
        ```
        {"artist": null, "auth": "Logged In", "firstName": "Walter", "gender": "M", "itemInSession": 0, "lastName": "Frye", "length": null, "level": "free", "location": "San Francisco-Oakland-Hayward, CA", "method": "GET","page": "Home", "registration": 1540919166796.0, "sessionId": 38, "song": null, "status": 200, "ts": 1541105830796, "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"", "userId": "39"}
        ```
      - Database Schema
        - songplays - records in log data associated with song plays (fact table)
          | songplay_id | start_time | user_id | level | song_id | artist_id | session_id | location | user_agent |  
          |---|---|---|---|---|---|---|---|---|
        - users - users in the app (dimension table)
          | user_id | first_name | last_name | gender | level |
          |---|---|---|---|---|
        - songs - songs in music database
          |song_id | title | artist_id | year | duration |
          |---|---|---|---|---|
        - artists - artists in music database
          |artist_id | name | location | latitude | longitude |
          |---|---|---|---|---|
        - time - timestamps of records in songplays broken down into specific units
          |start_time | hour | day | week | month | year | weekday |
          |---|---|---|---|---|---|---|
  <br>

  5. State and justify your database schema design and ETL pipeline
      - This is a database with star schema with `songplays` as fact table, dimemsion tables include `users`, `songs`, `artist` and `time`.
      - The ETL pipeline begins with creating database and tables using `python` with `psycopg2` library.
      - Then process song files and user log files in json format using `pandas`.
      - Finally insert processed dataframes into corresponding tables.

  <br>

