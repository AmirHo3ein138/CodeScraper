IF OBJECT_ID('dbo.Villas', 'U') IS NOT NULL DROP TABLE Villas;
IF OBJECT_ID('dbo.AlibabaRaw', 'U') IS NOT NULL DROP TABLE AlibabaRaw;

CREATE TABLE Villas( 
	ADname NVARCHAR(255),
	Price INT,
	GeneralInfo NVARCHAR(255)
	);

CREATE TABLE AlibabaRaw(
	Line NVARCHAR(MAX)
);

BULK INSERT AlibabaRaw
FROM 'F:\AP4032\websrapping_test\data_Alibaba.txt' -- directory to the extracted data file 
WITH (
	ROWTERMINATOR = '\n',
	CODEPAGE = '65001'
	);
	SET ANSI_WARNINGS OFF;

WITH GroupedLines AS (
	SELECT 
	Line,
	ROW_NUMBER() OVER (ORDER BY(SELECT NULL)) as ali
	FROM AlibabaRaw
	WHERE Line IS NOT NULL AND LTRIM(LTRIM(Line)) <> ''
	),
Parsed AS (
	Select 
		Max(Case WHEN ali % 4 = 1 then REPLACE(Line, 'Villa Name is: ', '') END) AS AD,
		MAX(CASE WHEN ali % 4 = 2 THEN CAST(REPLACE(REPLACE(Line, 'Villa Price for Every Night is: ', ''), ',' , '') as INT) END) AS Pr,
		Max(CASE WHEN ali % 4 = 3 THEN REPLACE(Line, 'Villa Basic Information is: ', '') END) AS info
		FROM GroupedLines
		Group by (ali - 1)/4)

INSERT INTO Villas(ADname, Price, GeneralInfo)
SELECT AD, Pr , info FROM Parsed;


SELECT * FROM Villas;


