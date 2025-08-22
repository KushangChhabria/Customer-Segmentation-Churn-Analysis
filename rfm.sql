WITH base AS (
    SELECT 
        CustomerID,
        InvoiceNo,
        InvoiceDate,
        (Quantity * UnitPrice) AS Amount
    FROM transactions
    WHERE CustomerID IS NOT NULL
),
rfm AS (
    SELECT
        CustomerID,
        -- Recency: difference between today and last invoice
        DATEDIFF(DAY, MAX(InvoiceDate), (SELECT DATEADD(DAY, 1, MAX(InvoiceDate)) FROM base)) AS Recency,
        
        -- Frequency: number of invoices
        COUNT(DISTINCT InvoiceNo) AS Frequency,
        
        -- Monetary: total amount spent
        SUM(Amount) AS Monetary
    FROM base
    GROUP BY CustomerID
),
rfm_scores AS (
    SELECT
        CustomerID,
        Recency,
        Frequency,
        Monetary,
        NTILE(5) OVER (ORDER BY Recency ASC) AS R_score,  -- smaller recency = higher score
        NTILE(5) OVER (ORDER BY Frequency DESC) AS F_score,
        NTILE(5) OVER (ORDER BY Monetary DESC) AS M_score
    FROM rfm
)
SELECT
    CustomerID,
    Recency,
    Frequency,
    Monetary,
    R_score,
    F_score,
    M_score,
    (R_score + F_score + M_score) AS RFM_Score,
    CASE 
        WHEN (R_score + F_score + M_score) >= 12 THEN 'Loyal Customer'
        WHEN (R_score + F_score + M_score) >= 9  THEN 'Potential Loyalist'
        WHEN (R_score + F_score + M_score) >= 6  THEN 'At Risk'
        ELSE 'Churn Risk'
    END AS Segment
FROM rfm_scores;
