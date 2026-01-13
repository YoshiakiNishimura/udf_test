drop table if exists t_decimal;
drop table if exists test;
drop table if exists t_two;
drop table if exists ta_two;
drop table if exists t_three;
drop table if exists t_blob;
-- tablemake
create table t_decimal (v decimal(15, 2));
create table t_two (d date, t time);
create table ta_two (stamp1 TIMESTAMP,stamp2 TIMESTAMP WITH TIME ZONE);
create table test (value3 DECIMAL(10,2), date1  DATE, time1  TIME,
  stamp1 TIMESTAMP,stamp2 TIMESTAMP WITH TIME ZONE,
  blob1  BLOB,clob1  CLOB);
create table t_three (blob1 BLOB, clob1 CLOB, stamp1 TIMESTAMP);
create table t_blob (b BLOB);
-- insert
insert into t_decimal values (1234.53);
insert into t_two values (date'2000-01-01', time'00:00:01');
insert into test values (1234.53,date'2000-01-01',time'00:00:01',
  timestamp'2001-01-01 11:22:33',
  timestamp with time zone'2000-01-02 11:22:33+09:00',
  X'1234','abc'
);
insert into ta_two values (timestamp'2001-01-01 11:22:33', timestamp with time zone'2000-01-02 11:22:33+09:00');
insert into t_three values (X'1234', 'abc', timestamp'2001-01-01 11:22:33');
insert into t_blob values (X'1234');
-- check
select inc_decimal(v) from t_decimal;
SELECT t_decimal.v,R.value FROM t_decimal CROSS APPLY stream_decimal(t_decimal.v) AS R(value);
select inc_two(d, t) from t_two;
select t_two.d, r.value from t_two cross apply stream_two(t_two.d, t_two.t) as r(value);
select inc_three(blob1, clob1, stamp1) from t_three;
select inc_blob(b) from t_blob;
select inc_another_two(stamp1, stamp2) from ta_two;
select ta_two.stamp1, r.value from ta_two cross apply stream_another_two(ta_two.stamp1, ta_two.stamp2) as r(value);
-- select inc_alltypes(value3, date1, time1, stamp1, stamp2, blob1, clob1) from test;
-- select t_blob.b, R.value FROM t_blob CROSS APPLY stream_blob(t_blob.b) AS R(value);
-- SELECT t_three.blob1, R.value FROM t_three CROSS APPLY stream_three(t_three.blob1, t_three.clob1, t_three.stamp1) AS R(value);
