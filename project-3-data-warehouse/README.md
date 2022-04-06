# Udacity Data Engineer Project 3: Data Warehouse on AWS


1. Project Description<br>
  In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

2. Project Template
    - `create_table.py` is where you'll create your fact and dimension tables for the star schema in Redshift.
    - `etl.py` is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
    - `sql_queries.py` is where you'll define you SQL statements, which will be imported into the two other files above.
    - `README.md` is where you'll provide discussion on your process and decisions for this ETL pipeline.

3. Project Steps
    - Create Table Schemas
        1. Design schemas for your fact and dimension tables
        2. Write a SQL CREATE statement for each of these tables in `sql_queries.py`
        3. Complete the logic in `create_tables.py` to connect to the database and create these tables
        4. Write SQL DROP statements to drop tables in the beginning of `create_tables.py` if the tables already exist. This way, you can run `create_tables.py` whenever you want to reset your database and test your ETL pipeline.
        5. Launch a redshift cluster and create an IAM role that has read access to S3.
        6. Add redshift database and IAM role info to `dwh.cfg`.
        7. Test by running `create_tables.py` and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
    - Build ETL Pipeline
        1. Implement the logic in `etl.py` to load data from S3 to staging tables on Redshift.
        2. Implement the logic in `etl.py` to load data from staging tables to analytics tables on Redshift.
        3. Test by running `etl.py` after running `create_tables.py` and running the analytic queries on your Redshift database to compare your results with the expected results.
        4. Delete your redshift cluster when finished.
<br>
<br>
---

1. Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
    - The purpose of the database is for the company to understand how their users in terms of who, when, what, and how in order to improve its service.
<br>
<br>
2. State and justify your database schema design and ETL pipeline.
    - Read data into 2 staging tables namely `staging_event` and `staging_songs`, from where generates 1 fact table and 4 dimension tables listed below:
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
<br>

3. Example queries and results for song play analysis.
    - User over the day: By running the query below we can discover that there are more users between 15:00 and 19:00 than other hours.
      ```
      SELECT B.hour, COUNT(DISTINCT A.user_id) FROM songplays A
      LEFT JOIN time B ON (A.start_time = B.start_time)
      GROUP BY B.hour
      ORDER BY B.hour
      ```
    - User over the week(0 as Sunday): By running the query below we can find out that there are less users on Saturday and Sunday.
      ```
      SELECT B.weekday, COUNT(DISTINCT A.user_id) FROM songplays A
      LEFT JOIN time B (ON A.start_time = B.start_time)
      GROUP BY B.weekday
      ORDER BY B.weekday
      ```
