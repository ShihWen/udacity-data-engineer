DROP TABLE IF EXISTS staging_traffic;
CREATE TABLE staging_traffic
(
  date        date,
  hour        smallint,
  entrance    varchar(20),
  exit        varchar(20),
  traffic     int
);

DROP TABLE IF EXISTS staging_station_exit;
CREATE TABLE staging_station_exit
(
  station_id         varchar(20)
  , exit_id          smallint
  , stair            boolean
  , escalator        smallint
  , elevator         boolean
  , station_name_zh  varchar(20)
  , station_name_en  varchar(50)
  , exit_name_zh     varchar(50)
  , exit_name_en     varchar(50)
  , exit_longitude   DECIMAL(9,6)
  , exit_latitude    DECIMAL(9,6)
  , exit_geohash     varchar(20)
  , version_id       varchar(10)
  , station_join_key varchar(20)
);

DROP TABLE IF EXISTS staging_station;
CREATE TABLE staging_station
(
  station_id              varchar(20)
  , station_address       varchar(200)
  , bike_allow_on_holidy  boolean
  , location_city         varchar(20)
  , location_city_code    varchar(10)
  , station_name_zh       varchar(20)
  , station_name_en       varchar(50)
  , station_longitude     DECIMAL(9,6)
  , station_latitude      DECIMAL(9,6)
  , station_geohash       varchar(20)
  , version_id            varchar(10)
  , station_join_key      varchar(20)
);

DROP TABLE IF EXISTS mrt_station_dim;
CREATE TABLE mrt_station_dim
(
  station_key             integer identity(0,1)
  , station_id            varchar(20)
  , station_address       varchar(200)
  , bike_allow_on_holidy  boolean
  , location_city         varchar(20)
  , location_city_code    varchar(10)
  , station_name_zh       varchar(20)
  , station_name_en       varchar(50)
  , station_longitude     DECIMAL(9,6)
  , station_latitude      DECIMAL(9,6)
  , station_geohash       varchar(20)
  , version_id            varchar(20)
  , station_join_key      varchar(20)
  , update_date           datetime
);

DROP TABLE IF EXISTS mrt_station_exit_dim;
CREATE TABLE mrt_station_exit_dim
(
  exit_key           integer identity(0,1)
  , station_id       varchar(20)
  , exit_id          smallint
  , stair            boolean
  , escalator        smallint
  , elevator         boolean
  , station_name_zh  varchar(20)
  , station_name_en  varchar(50)
  , exit_name_zh     varchar(50)
  , exit_name_en     varchar(50)
  , exit_longitude   DECIMAL(9,6)
  , exit_latitude    DECIMAL(9,6)
  , exit_geohash     varchar(20)
  , version_id       varchar(20)
  , station_join_key varchar(20)
  , update_date      datetime
);

DROP TABLE IF EXISTS time_dim;
CREATE TABLE time_dim
(
  time_key       integer identity(0,1)
  , time         datetime
  , year         integer
  , month        smallint
  , day          smallint
  , hour         smallint
  , day_of_week  smallint
  , week_of_year smallint
  , update_date datetime
);

DROP TABLE IF EXISTS mrt_traffic_fact;
CREATE TABLE mrt_traffic_fact
(
  time_key                  integer
  , entrance_station_key    integer
  , exit_station_key        integer
  , traffic                 integer
  , update_date             datetime
);