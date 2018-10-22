
--To find better Primary Index make use of below query which gives you the data distribution details across all AMP. Make sure data is distributed evenly across all AMP.

SEL HASHAMP(HASHBUCKET(HASHROW(column1))) as AMP , COUNT(*) Record_count FROM databasename .tablename GROUP BY 1;
--(or)
SEL HASHAMP(HASHBUCKET(HASHROW( column1, coulmn2 ,....))) as AMP , COUNT(*) FROM databasename .tablename GROUP BY 1;

--Record_count: Total number of records distributed in each AMP.
--Note: Try to define Primary Index on joining column if its doesn't hold more duplicated records
