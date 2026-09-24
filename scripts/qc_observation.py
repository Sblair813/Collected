--  "description": "QC Type Totals for multiple Days",
USE AAD;
GO
DECLARE @Sdate DATE = '09/05/2024'
--CAST(GETDATE()-3 AS DATE)
DECLARE @Edate DATE = CAST(GETDATE()-1 AS DATE)
SELECT 'NC' AS 'FC',CAST(d.AddDate AS DATE) AS qc_date,ISNULL(qc.Description, 'Total') AS qc_type,  
COUNT(1) container_count
FROM(SELECT *,ROW_NUMBER() OVER (PARTITION BY ContainerId ORDER BY AddDate DESC) AS row_rank
FROM vitaqc.tblContainerLog WITH(NOLOCK)  
WHERE ContainerId IS NOT NULL
AND QcCompleted = 1)  
JOIN vitaqc.tblQualityControlType qc WITH(NOLOCK)        
ON qc.QualityControlType = d.QualityControlType
WHERE CAST(d.AddDate AS DATE) between @Sdate AND @Edate  
AND d.row_rank = 1
GROUP BY qc.Description ,CAST(d.AddDate AS DATE) WITH CUBE;"
