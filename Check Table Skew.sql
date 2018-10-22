SEL databasename,TABLENAME,SUM(currentperm)/1024**3 SizeGB,
(100 - (AVG(CurrentPerm)/NULLIFZERO(MAX(CurrentPerm))*100)) SkewFactor_in_percentage
FROM dbc.tablesize 
WHERE DatabaseName='sandbox' AND TABLENAME='evan_b2'
GROUP BY 1,2 ORDER BY 1,2;
