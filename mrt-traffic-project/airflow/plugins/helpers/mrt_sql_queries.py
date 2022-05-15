class MrtSqlQueries:
    # insert tables
    insert_station_dim = ("""
        INSERT INTO mrt_station_dim
        (
            station_id
            , station_address
            , bike_allow_on_holidy
            , location_city
            , location_city_code
            , station_name_zh
            , station_name_en
            , station_longitude
            , station_latitude
            , station_geohash
            , version_id
            , station_join_key
            , update_date 
        )
        SELECT   station_id
                , station_address
                , bike_allow_on_holidy
                , location_city
                , location_city_code
                , station_name_zh
                , station_name_en
                , station_longitude
                , station_latitude
                , station_geohash
                , version_id
                , station_join_key
                , GETDATE()
        FROM staging_station;
    """)

    insert_station_exit_dim = ("""
        INSERT INTO mrt_station_exit_dim
        (
            station_id
            , exit_id
            , stair
            , escalator
            , elevator
            , station_name_zh
            , station_name_en
            , exit_name_zh
            , exit_name_en
            , exit_longitude
            , exit_latitude
            , exit_geohash
            , version_id
            , station_join_key
            , update_date
        )
        SELECT   station_id
                , exit_id
                , stair
                , escalator
                , elevator
                , station_name_zh
                , station_name_en
                , exit_name_zh
                , exit_name_en
                , exit_longitude
                , exit_latitude
                , exit_geohash
                , version_id
                , station_join_key
                , GETDATE()
        FROM staging_station_exit;
    """)

    insert_time_dim = ("""
        INSERT INTO time_dim
        (
            time
            , year
            , month
            , day
            , hour
            , day_of_week
            , week_of_year
            , update_date
        )
        SELECT DISTINCT DATEADD(hour,hour,date)
                , EXTRACT( YEAR FROM date)
                , EXTRACT( MONTH FROM date)
                , EXTRACT( DAY FROM date)
                , hour
                , DATE_PART(dow, date) 
                , DATE_PART(w, date) 
                , GETDATE()
        FROM staging_traffic;
    """)

    insert_traffic_fact = ("""
        INSERT INTO mrt_traffic_fact
        (
            time_key
            , entrance_station_key
            , exit_station_key
            , traffic
            , update_date
        )
        SELECT B.time_key
            , in_station.station_key AS entrance_station_key 
            , out_station.station_key AS exit_station_key
            , traffic
            , GETDATE()
        FROM staging_traffic A
        LEFT JOIN time_dim B ON (DATEADD(hour,A.hour,date) = B.time)
        LEFT JOIN mrt_station_dim in_station ON (A.entrance = in_station.station_join_key)
        LEFT JOIN mrt_station_dim out_station ON (A.exit = out_station.station_join_key);
    """)
    
    create_transfer_station_dim = ("""
        DROP TABLE IF EXISTS mrt_transfer_station_dim;
        WITH transfer_station AS
        (
          SELECT station_name_zh
          FROM
          (
            SELECT station_name_zh
                   , station_id
                   , ROW_NUMBER() OVER(PARTITION BY station_name_zh ORDER BY station_id) AS RN
            FROM mrt_station_dim
          ) X
          WHERE rn > 1
        )
        SELECT station_key
               , station_id
               , station_name_zh
               , station_name_en
               , GETDATE()
        INTO mrt_transfer_station_dim
        FROM mrt_station_dim A
        WHERE EXISTS
        (
          SELECT station_name_zh
          FROM transfer_station B
          WHERE A.station_name_zh = B.station_name_zh
        )
        ORDER BY station_name_zh, station_id
    """)
    
    check_fact_table = ("""
        SELECT COUNT(*)
        FROM
        (
        SELECT C.time
               --, A.entrance_station_key
               , D.station_name_zh as entrance_station
               --, D.station_id as entrance_id
               , A.exit_station_key
               , B.station_name_zh as exit_station
               , B.station_id as exit_id
               , A.traffic
        FROM mrt_traffic_fact A
        LEFT JOIN mrt_station_dim B ON A.exit_station_key = B.station_key
        LEFT JOIN mrt_station_dim D ON A.entrance_station_key = D.station_key
        LEFT JOIN time_dim C ON A.time_key = C.time_key
        WHERE D.station_name_zh = '松山機場'
        AND C.time = '2022-02-01 12:00'
        ORDER BY C.time, B.station_name_zh
        ) X
    """)
    check_fact_table_pure = ("""
        SELECT A.time_key
               , A.entrance_station_key
               , A.exit_station_key
               , A.traffic
        FROM mrt_traffic_fact A
        WHERE 1=1
        AND A.entrance_station_key = 610
        AND A.time_key = 187
    """)
    
    check_station_number_dim = ("""
       SELECT COUNT(*)
       FROM mrt_station_dim
    """)

    check_station_number_stagin = ("""
       SELECT COUNT(*)
       FROM staging_station
    """)
