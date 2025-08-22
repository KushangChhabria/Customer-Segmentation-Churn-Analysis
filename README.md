# Customer Segmentation & Churn Analysis

## Project Description
This project performs **Customer Segmentation and Churn Analysis** using transactional data from an online retail dataset.  
It identifies high-value customers, potential loyalists, at-risk customers, and churn risks using **RFM (Recency, Frequency, Monetary) analysis**, and visualizes insights through **interactive Power BI dashboards**.

---

## Tech Stack
- **Python:** pandas, datetime, matplotlib, seaborn  
- **SQL:** For RFM calculations in a database environment  
- **Power BI:** For interactive dashboards and KPI visuals  

---

## Project Workflow

### 1. Data Loading & Preprocessing (Python)
- Load `Online Retail.xlsx`.  
- Drop missing `CustomerID`.  
- Compute `TotalAmount = Quantity * UnitPrice`.  
- Convert `InvoiceDate` to datetime format.  
- Set reference date for recency calculations.

### 2. RFM Calculation (Python & SQL)
- Compute **Recency, Frequency, and Monetary** for each customer.  
- Assign **R, F, M scores** using quintiles.  
- Combine scores into `RFM_Score` and segment customers into:
  - Loyal Customer
  - Potential Loyalist
  - At Risk
  - Churn Risk  
- Export results to `rfm_segments.csv`.

SQL version (for database):  
- Use `NTILE(5)` to calculate R, F, M scores.  
- Calculate `RFM_Score` and assign segments with `CASE WHEN` statements.

### 3. Power BI Dashboard

#### Power Query & Data Preparation
- Ensure column types:
  - `CustomerID` → Whole Number / Text  
  - `Recency, Frequency` → Whole Number  
  - `Monetary` → Decimal  
  - `R_score, F_score, M_score, RFM_Score` → Whole Number  
  - `Segment, RFM_Segment` → Text  
- Apply → Close & Apply

#### Measures (DAX)
- Total Customers, Segment-wise counts: Loyal, At Risk, Churn Risk, Potential Loyalists  
- Percentages: `% Loyal`, `% At Risk`, etc.  
- Monetary metrics: `Total Monetary`, `Avg Monetary per Customer`  
- Other metrics: `Avg Recency`, `Avg Frequency`  

#### Report Layout
- **KPI Cards:** Customers, % Loyal, % At Risk, % Churn Risk, Avg Monetary per Customer  
- **Bar Chart:** Customer count by segment  
- **Donut Chart:** Segment share (%)  
- **Table:** Top customers with conditional formatting on Monetary  
- **Scatter Plot (Optional):** Frequency vs Monetary by Segment  
- **Slicers:** Segment (optional: R_score, F_score, M_score)  

#### Formatting Tips
- Turn on data labels where needed  
- Rename visuals for clarity  
- Apply clean theme  

---

## Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/YourUsername/Customer-Segmentation-Churn.git
```
2. **Install dependencies:**
```bash
pip install pandas matplotlib seaborn openpyxl
```
3. **Run the Python script:**
```bash
python main.py
```
4. Open the generated rfm_segments.csv in Power BI.
5. Build visuals as described above to explore customer segmentation and churn.

## Output

- rfm_segments.csv containing RFM metrics and customer segments
- Python visualizations: bar plots, pie charts, boxplots
- Power BI dashboard with KPI cards, charts, tables, and slicers

## Acknowledgements

- Dataset: Online Retail Dataset
- Python libraries: pandas, matplotlib, seaborn
- Power BI for dashboards
