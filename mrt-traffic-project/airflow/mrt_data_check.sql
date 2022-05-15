select count(*)
from
(
select C.time
       --, A.entrance_station_key
       , D.station_name_zh as entrance_station
       --, D.station_id as entrance_id
       , A.exit_station_key
	   , B.station_name_zh as exit_station
       , B.station_id as exit_id
       , A.traffic
from mrt_traffic_fact A
left join mrt_station_dim B on A.exit_station_key = B.station_key
left join mrt_station_dim D on A.entrance_station_key = D.station_key
left join time_dim C on A.time_key = C.time_key
where D.station_name_zh = '松山機場'
and C.time = '2022-02-01 12:00'
order by C.time, B.station_name_zh
) X