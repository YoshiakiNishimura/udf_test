drop table if exists t_ap;
drop table if exists t_ref;
-- tablemake
create table t_ap (a int, b int);
create table t_ref (a int, c int);
-- insert
insert into t_ap (a, b) VALUES (1, 10),(2, 20);
insert into t_ref (a, c) VALUES (1, 30),(2, 40);
-- check
select ap.a, new_ref.c2 from t_ap as ap APPLY app_func(ap.a) as new_ref
-- select a , b from t_ap;
-- select ap.a,ap.b, re.c from t_ap as ap inner join t_ref as re on ap.a = re.a;
--select * from t_ap;
