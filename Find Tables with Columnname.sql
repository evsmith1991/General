
-----Teradata-----
SELECT databasename, tablename FROM dbc.columns WHERE columnname LIKE '%place_uuid%' ;


-----Cerebro-----
select distinct database_name, table_name from cerebro_metadata.table_metadata where database_name='dw' and table_name like '%traffic%';
