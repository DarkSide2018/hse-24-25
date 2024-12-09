CREATE TABLE RVGA_LOG_REPORT as 
with true_ip as (
  SELECT split_part(data, '	', 2) as region,
  split_part(data, '	', 1) as ip,
  data as ip_data
     FROM De.IP 
),de_ip as (
  SELECT region,
  ip ,
  split_part(ip, '.', 1)::int,
  ip_data
     FROM true_ip
      WHERE  split_part(ip, '.', 1)::int < 256
      and split_part(ip, '.', 2)::int < 256
       and split_part(ip, '.', 3)::int < 256
        and split_part(ip, '.', 4)::int < 256
), log_table as (
SELECT
    to_timestamp(substring(de_log.data from '\d{14}')::text, 'YYYYMMDDHH24MISS') AS DT,
    substring(de_log.data from 'http[s]?://[^ ]+') AS LINK,
    substring(de_log.data from '[^ ]+$') AS USER_AGENT,
    split_part(de_log.data,'	',1) as log_ip,
    de_ip.region,
    de_ip.ip
FROM
    DE.LOG as de_log join de_ip on split_part(de_log.data,'	',1) = de_ip.ip
), sub_query as (
  SELECT REGION,
           USER_AGENT,
           ROW_NUMBER() OVER (PARTITION BY REGION ORDER BY COUNT(*) DESC) AS rn
    FROM log_table
    GROUP BY REGION, USER_AGENT
)
select REGION,
USER_AGENT 
from sub_query
where rn=1;









CREATE TABLE RVGA_LOG as 
with true_ip as (
  SELECT split_part(data, '	', 2) as region,
  split_part(data, '	', 1) as ip,
  data as ip_data
     FROM De.IP 
),de_ip as (
  SELECT region,
  ip ,
  split_part(ip, '.', 1)::int,
  ip_data
     FROM true_ip
      WHERE  split_part(ip, '.', 1)::int < 256
      and split_part(ip, '.', 2)::int < 256
       and split_part(ip, '.', 3)::int < 256
        and split_part(ip, '.', 4)::int < 256
)
SELECT
    to_timestamp(substring(de_log.data from '\d{14}')::text, 'YYYYMMDDHH24MISS') AS DT,
    substring(de_log.data from 'http[s]?://[^ ]+') AS LINK,
    substring(de_log.data from '[^ ]+$') AS USER_AGENT,
    de_ip.region as REGION
FROM
    DE.LOG as de_log join de_ip on split_part(de_log.data,'	',1) = de_ip.ip