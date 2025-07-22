# Importing the required libraries.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Loading the dataset
try:
    df = pd.read_csv("Insurance_sales_data.csv")
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'Insurance_sales_data.csv' not found.")
    exit()

# Changing date formate
df['Sale_Date']=pd.to_datetime(df['Sale_Date'], format = '%Y-%m-%d',dayfirst=True)
df['Policy_Start_Date'] = pd.to_datetime(df['Policy_Start_Date'],format = '%Y-%m-%d', dayfirst=True)
df['Policy_End_Date'] = pd.to_datetime(df['Policy_End_Date'],format = '%Y-%m-%d', dayfirst=True)

# Create new time-based features
df['Sale_Month'] = df['Sale_Date'].dt.month_name()
df['Sale_Quarter'] = df['Sale_Date'].dt.quarter
df['Sale_Year'] = df['Sale_Date'].dt.year

# Calculating the policy duration
df['Policy_Duration_Days'] = (df['Policy_End_Date'] - df['Policy_Start_Date']).dt.days
df['Policy_Duration_Years'] = df['Policy_Duration_Days'] / 365.25

# Create Age Group for analysis
age_bins = [18, 25, 35, 45, 55, 65, 75, np.inf]
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
df['Age_Group'] = pd.cut(df['Customer_Age'], bins=age_bins, labels=age_labels, right=False)

print("\n--- Ready For Advanced Data Analysis ---\n")

# Monthly sales of policies and the total premium collected from them.

df['Month_Name']= df['Sale_Date'].dt.strftime('%B')
df['Month_Num']= df['Sale_Date'].dt.month

Month_sales = df.groupby(['Month_Name', 'Financial_Year','Month_Num']).agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum'),
    Total_Claim = ('Claim_Amount','sum')
).reset_index()

Month_sales = Month_sales.sort_values('Month_Num')
FY = Month_sales['Financial_Year'].unique()

for f in FY:
    data = Month_sales[Month_sales['Financial_Year']== f]

    plt.figure(figsize=(15, 10))
    plt.subplot(2, 1, 1)
    sns.lineplot(y='Total_Policies', x='Month_Name', data=data, marker='o', color='green')
    plt.xlabel('Months')
    plt.ylabel('Total Policies sold')
    plt.xticks(rotation=45)
    plt.title(f'Total Policies sold over months in {f}')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.subplot(2, 1, 2)
    sns.lineplot(y='Total_Premium', x='Month_Name', data=data, marker='o', color='green')
    plt.xlabel('Months')
    plt.ylabel('Total Premium')
    plt.xticks(rotation=45)
    plt.title(f'Total Premium collected over months in {f}')
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Quarterly Sales Distribution by Policy Type
# Just creating a table in wide format with below-mentioned as the column name and premium amount
Quarter_sale = df.groupby(['Sale_Year','Sale_Quarter','Policy_Type'])['Premium_Amount'].sum().unstack(fill_value = 0).reset_index()

# Melting the row in long table formate into wide format which we will use to draw graphs
Quarter_sale_melt = Quarter_sale.melt( id_vars=['Sale_Year','Sale_Quarter'], var_name='Policy_Type', value_name='Total_Premium')

# We are making new column basis which we will plot the graph.
Quarter_sale_melt['Year_Quarter'] = Quarter_sale_melt['Sale_Year'].astype(str) +' -Q' + Quarter_sale_melt['Sale_Quarter'].astype(str)

plt.figure(figsize=(15, 8))
sns.barplot(x='Year_Quarter', y='Total_Premium', hue='Policy_Type', data= Quarter_sale_melt, palette='viridis')
plt.title('Quarterly Premium Contribution by Policy Type')
plt.xlabel('Year-Quarter')
plt.ylabel('Total Premium (INR)')
plt.xticks(rotation=45)
plt.legend(title='Policy Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Coverage Amount distribution by Policy Type (Box Plot)
plt.figure(figsize=(14, 8))
sns.boxplot(x='Policy_Type', y='Coverage_Amount', data=df, palette='GnBu')
plt.title('Distribution of Coverage Amount by Policy Type')
plt.xlabel('Policy Type')
plt.ylabel('Coverage Amount (INR)')
plt.ylim(0, df['Coverage_Amount'].quantile(0.99)) # Limit y-axis to focus on main distribution
plt.tight_layout()
plt.show()

# Policy Duration Distribution by Policy Type
plt.figure(figsize=(14, 8))
sns.violinplot(x='Policy_Type', y='Policy_Duration_Years', data=df, inner='quartile', palette='pastel')
plt.title('Distribution of Policy Duration by Policy Type')
plt.xlabel('Policy Type')
plt.ylabel('Policy Duration (Years)')
plt.ylim(0, df['Policy_Duration_Years'].quantile(0.99))
plt.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray')
plt.tight_layout()
plt.show()


# We will analyze the relationship between two or more categorical variables like sales channel and policy type using crosstab of Pandas

PC_crosstab = pd.crosstab(df['Policy_Type'],df['Sales_Channel'], normalize = 'columns') # Normalize by column to see channel preference
PG_crosstab = pd.crosstab(df['Policy_Type'],df['Customer_Gender'], normalize = 'columns')
GS_crosstab = pd.crosstab(df['Customer_Gender'],df['Sales_Channel'], normalize = 'columns')

# Give Heat map of sales channel and policy type
plt.figure(figsize=(10, 8))
sns.heatmap(PC_crosstab, annot=True, cmap='YlGnBu', fmt=".2f", linewidths=.5)
plt.title('Distribution of Policy Types Across Sales Channels (Column Normalized)')
plt.ylabel('Policy Type')
plt.xlabel('Sales Channel')
plt.tight_layout()
plt.show()

# Give Heat map of customer gender and policy type
plt.figure(figsize=(10, 8))
sns.heatmap(PG_crosstab, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
plt.title('Distribution of Policy Types Across Customer Gender (Column Normalized)')
plt.ylabel('Policy Type')
plt.xlabel('Customer Gender')
plt.tight_layout()
plt.show()

# Give Heat map of customer gender and sales channel
plt.figure(figsize=(10, 8))
sns.heatmap(GS_crosstab, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Distribution of Sales Channel Across Customer Gender (Column Normalized)')
plt.ylabel('Sales Channel')
plt.xlabel('Customer Gender')
plt.tight_layout()
plt.show()


# Claim Rate by Age Group and Policy Type
claim_rate_pivot = df.groupby(['Age_Group', 'Policy_Type'])['Has_Claimed'].mean().unstack()
print("\nClaim Rate by Age Group and Policy Type:")
# print(claim_rate_pivot)

plt.figure(figsize=(14, 8))
sns.heatmap(claim_rate_pivot, annot=True, cmap='RdYlGn_r', fmt=".2f", linewidths=.5)
plt.title('Average Claim Probability by Age Group and Policy Type')
plt.ylabel('Age Group')
plt.xlabel('Policy Type')
plt.tight_layout()
plt.show()









