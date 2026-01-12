drop table if exists T;
drop table if exists T2;

-- tablemake
CREATE TABLE T (C0 BIGINT PRIMARY KEY, C1 BIGINT);
CREATE TABLE T2 (C0 INT PRIMARY KEY, I32 INT, F REAL,D DOUBLE);
-- insert
INSERT INTO T VALUES (1, 100);
INSERT INTO T VALUES (2, 200);
INSERT INTO T2 VALUES (1,  7,  1.5, 10.25);
INSERT INTO T2 VALUES (2, 99,  2.0,  3.14);
-- check
SELECT T.C0,T.C1,R.value FROM T CROSS APPLY app_func(T.C0) AS R(value);
SELECT T2.C0,T2.I32,T2.F,T2.D,R.value FROM T2 CROSS APPLY app_func2(T2.C0,T2.F,T2.D) AS R(value);
-- SELECT T.C0, T.C1, R.c1, R.c2 FROM T CROSS APPLY (T.C0) AS R(c1, c2);
-- select * from t_ap apply app_func(t_ap.a)  as u1
-- select a , b from t_ap;
-- select ap.a,ap.b, re.c from t_ap as ap inner join t_ref as re on ap.a = re.a;
--select * from t_ap;
