
IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ads]') AND type = N'U'
)
BEGIN
    CREATE TABLE dbo.ads (
        ad_id       INT IDENTITY(1,1) PRIMARY KEY,
        source      NVARCHAR(50),
        name        NVARCHAR(500),
        price       NVARCHAR(100),
        owner       NVARCHAR(200),
        description NVARCHAR(MAX),
        features    NVARCHAR(MAX),
        url         NVARCHAR(1000)
    );
END;

IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[similar_ads]') AND type = N'U'
)
BEGIN
    CREATE TABLE dbo.similar_ads (
        match_id   INT IDENTITY(1,1) PRIMARY KEY,
        ad1_id     INT NOT NULL REFERENCES dbo.ads(ad_id),
        ad2_id     INT NOT NULL REFERENCES dbo.ads(ad_id),
        similarity DECIMAL(5,2)
    );
END;



IF OBJECT_ID('tempdb..#raw') IS NOT NULL
    DROP TABLE #raw;

CREATE TABLE #raw (
    line_no INT IDENTITY(1,1) PRIMARY KEY,
    txt     NVARCHAR(MAX)
);

INSERT INTO #raw (txt)
SELECT BulkColumn
FROM OPENROWSET(
       BULK N'F:\AP4032\seyed\similarity.txt', 
       SINGLE_CLOB, 
       CODEPAGE = '65001'
     ) AS x;



IF OBJECT_ID('tempdb..#splits') IS NOT NULL DROP TABLE #splits;
SELECT *,
       grp = SUM(CASE WHEN txt LIKE '===%' THEN 1 ELSE 0 END)
               OVER (ORDER BY line_no ROWS UNBOUNDED PRECEDING)
INTO #splits
FROM #raw;


IF OBJECT_ID('tempdb..#blocks') IS NOT NULL DROP TABLE #blocks;
SELECT
    grp,
    MIN(line_no) AS start_ln,
    MAX(line_no) AS end_ln
INTO #blocks
FROM #splits
WHERE grp > 0
GROUP BY grp;


INSERT INTO dbo.ads (source, name, price, owner, description, features, url)
SELECT
    CASE WHEN ad_data.ad_idx = 1 THEN 'site1' ELSE 'site2' END,
    ad_data.x.value('(./Name)[1]', 'NVARCHAR(500)'),
    ad_data.x.value('(./Price)[1]', 'NVARCHAR(100)'),
    ad_data.x.value('(./Owner)[1]', 'NVARCHAR(200)'),
    ad_data.x.query('.'),
    ad_data.x.value('(./Features)[1]', 'NVARCHAR(MAX)'),
    ad_data.x.value('(./URL)[1]', 'NVARCHAR(1000)')
FROM #blocks b
CROSS APPLY (
    SELECT
        '<root>' +
        REPLACE(
            (
                SELECT s.txt + CHAR(13)
                FROM #splits s
                WHERE s.grp = b.grp
                ORDER BY s.line_no
                FOR XML PATH(''), TYPE
            ).value('.', 'NVARCHAR(MAX)'),
            '&', '&amp;'
        ) + '</root>' AS xml_string
) AS xml_data
CROSS APPLY (
    SELECT CAST(xml_data.xml_string AS XML) AS doc
) AS xml_block
CROSS APPLY xml_block.doc.nodes('/root/br') AS ad_nodes(N)
CROSS APPLY (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS ad_idx,
        N.query('.') AS x
) AS ad_data;
SELECT * FROM similar_ads ORDER BY similarity DESC;
