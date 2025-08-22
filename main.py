import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


# Step 1: Load and preprocess

df = pd.read_excel("Online Retail.xlsx")

# Drop missing CustomerIDs
df = df.dropna(subset=['CustomerID'])

# Create TotalAmount column
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Reference date
today = df['InvoiceDate'].max() + dt.timedelta(days=1)

# Step 2: RFM Calculation

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (today - x.max()).days,
    'InvoiceNo': 'count',
    'TotalAmount': 'sum'
}).reset_index()

rfm.rename(columns={'InvoiceDate':'Recency','InvoiceNo':'Frequency','TotalAmount':'Monetary'}, inplace=True)

# Scores
rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

# Combine
rfm['RFM_Segment'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)
rfm['RFM_Score'] = rfm[['R_score','F_score','M_score']].sum(axis=1).astype(int)

# Segments
def segment_customer(row):
    if row['RFM_Score'] >= 12:
        return 'Loyal Customer'
    elif row['RFM_Score'] >= 9:
        return 'Potential Loyalist'
    elif row['RFM_Score'] >= 6:
        return 'At Risk'
    else:
        return 'Churn Risk'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print(rfm['Segment'].value_counts())

# Step 3: Export results

rfm.to_csv("rfm_segments.csv", index=False)

# Step 4: Visualizations

# Bar plot: segment counts
plt.figure(figsize=(8,5))
sns.countplot(x='Segment', data=rfm, order=rfm['Segment'].value_counts().index, palette="viridis")
plt.title("Customer Segments Distribution")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# Pie chart
plt.figure(figsize=(6,6))
rfm['Segment'].value_counts().plot.pie(autopct='%1.1f%%', colors=sns.color_palette("viridis", 4))
plt.title("Customer Segments Proportion")
plt.ylabel("")
plt.show()

# Boxplots: RFM metrics by segment
plt.figure(figsize=(12,4))
for i, metric in enumerate(['Recency','Frequency','Monetary']):
    plt.subplot(1,3,i+1)
    sns.boxplot(x='Segment', y=metric, data=rfm, palette="viridis")
    plt.title(f"{metric} by Segment")
    plt.xticks(rotation=30)

plt.tight_layout()
plt.show()
