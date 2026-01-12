drop table if exists t_decimal;
create table t_decimal (v decimal(15, 2));
insert into t_decimal values (1234.53);
select inc_decimal(v) from t_decimal;