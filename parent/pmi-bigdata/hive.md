USE movs2024a020_test;
DROP TABLE IF EXISTS Subnets;

CREATE EXTERNAL TABLE Subnets (
ip STRING,
mask STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY  '\t'
STORED AS TEXTFILE
LOCATION '/data/subnets/variant1';


check created table

hive --database movs2024a020_test -e 'SELECT * FROM Subnets LIMIT 10'


create partitioned table 

SET hive.exec.dynamic.partition.mode=nonstrict;

USE movs2024a020_test;

DROP TABLE IF EXISTS SubnetsPart;

CREATE EXTERNAL TABLE SubnetsPart (
ip STRING
)
PARTITIONED BY (mask STRING)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE SubnetsPart PARTITION (mask)
SELECT * FROM Subnets;



parse data with regular expressions

add jar /opt/cloudera/parcels/CDH/lib/hive/lib/hive-serde.jar;
USE movs2024a020_test;
DROP TABLE IF EXISTS SerDeExample;

CREATE EXTERNAL TABLE SerDeExample (
ip STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
"input.regex" = '^(\\S*)\\t.*$'
)
STORED AS TEXTFILE
LOCATION '/data/user_logs/user_logs_M';

select * from SerDeExample limit 10;
