# Importing the required libraries.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# We will be widely using seaborn to plot charts and matplotlib to give different configuration to enhance the charts views
# Use Pandas to read CSV and get the data basis which we will plot different graphs
# Used Numpy to create an array of age groups which we will use in our analysis

# Here we are trying to read our source file, if it is not there it will give an error
CSV = "Insurance_sales_data.csv"
try:
    df = pd.read_csv('Insurance_sales_data.csv')
    print(f"Data loaded Successfully, Ready to Plot:- \n")
except FileNotFoundError:
    print(f"Error: {CSV} not found.")


# While plotting the graph we change the date formate as per our further requirements.
df = pd.read_csv('Insurance_sales_data.csv')
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"], dayfirst=True)
df["Policy_Start_Date"]=pd.to_datetime(df["Policy_Start_Date"],dayfirst=True)
df["Policy_End_Date"]=pd.to_datetime(df["Policy_End_Date"],dayfirst=True)

df['Sale_Month'] = df['Sale_Date'].dt.month_name()
df['Sale_Quarter'] = df['Sale_Date'].dt.quarter
df['Sale_Year'] = df['Sale_Date'].dt.year

# Calculate policy duration
df['Policy_Duration_Days'] = (df['Policy_End_Date'] - df['Policy_Start_Date']).dt.days
df['Policy_Duration_Years'] = df['Policy_Duration_Days'] / 365.25

# These are the Palettes colour which we will be using to plot
# palettes = ["deep", "muted", "bright", "pastel", "dark", "colorblind",
#             "husl", "hls", "cubehelix", "Reds", "Blues", "Greens", "Purples",
#             "Oranges", "BuPu", "YlGnBu", "viridis", "plasma", "magma", "coolwarm"]


# 1.a - Analyze the total premium amount and number of policies sold each financial year

# Summary of the total policy sold in every Financial years and the premium collected
Sales_fy= df.groupby("Financial_Year").agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum')
).sort_values('Financial_Year').reset_index()
print("\n1.a - Sales by Financial Year:")
print(Sales_fy)

# plotting a bar graph showing the count of policy sold in all Financial years
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 2)
sns.barplot(
    x='Financial_Year',
    y='Total_Policies',
    data=Sales_fy,
    hue='Financial_Year',
    palette='viridis'
)
plt.title('Total Policies Sold per Financial Year')
plt.ylabel('Number of Policies')

# A barplot to show the total premium collected in all the Financial years
plt.subplot(1, 2, 1)
sns.barplot(
    x='Financial_Year',
    y='Total_Premium',
    data=Sales_fy,
    hue='Financial_Year',
    palette='magma',
    legend=False
)
plt.title('Total Premium Amount per Financial Year')
plt.ylabel('Total Premium (INR)')
plt.tight_layout()
plt.show()

# 1.b - Identify the most popular policy types and their contribution to total premiums

# Summary
Sales_fy_Policy= df.groupby("Policy_Type").agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum')
).sort_values('Total_Premium',ascending=False ).reset_index()
print("\n1.b - Most popular policy in the Financial Year:")
print(Sales_fy_Policy)

# Plotting a graph showing the different policy types and the count of the them sold
plt.figure(figsize=(12, 5))
plt.subplot(1,2,1)
sns.barplot(
    x='Policy_Type',
    y='Total_Policies',
    data=Sales_fy_Policy,
    hue='Policy_Type',
    palette='viridis',
    legend=False
)
plt.title('Total Policies Sold by Policy Type')
plt.ylabel('Number of Policies')
plt.xlabel('Policy Type')
plt.tight_layout()
plt.xticks(rotation=45)

# Plotting a graph showing the different policy types and the premium collected
plt.subplot(1,2,2)
sns.barplot(
    x='Policy_Type',
    y='Total_Premium',
    data=Sales_fy_Policy,
    hue='Policy_Type',
    palette='cubehelix',
    legend=False
)
plt.title('Total Premium to the Policy Type')
plt.xlabel('Policy Type')
plt.ylabel('Total Premium in Millions')
plt.xticks(rotation=45) #it rotates the names of the bars of the X-asis to 45 degree
plt.tight_layout()
plt.show()


# 1.c - Examine sales trends across different policy types over the three financial years

# Creating a Pie chart which will show the contribution of policy types in the sales of any financial year.
plt.figure(figsize=(8, 4))
plt.pie(
    x=Sales_fy_Policy['Total_Premium'],
    labels= Sales_fy_Policy['Policy_Type'],
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    explode= [0.02,0.02,0.02,0.02,0.02] ,
    colors=sns.color_palette('pastel')
)
plt.title('Percentage of Total Premium by Policy Type')
plt.axis('equal')
plt.tight_layout()
plt.show()

# 2.a Understand the age distribution of policyholders.

plt.figure(figsize = (10,10))
sns.histplot(
    df['Customer_Age'],
    bins=10,
    element= "poly",
    stat='count',
    kde=True,
    color='red'
)
plt.title('Distribution of Customer Age')
plt.xlabel('Customer Age')
plt.ylabel('Number of Customers')
plt.show()

# 2.b Explore how gender and age influence policy purchases and premium amounts.

# Making a dictionary and a function to use further to compare data at several age groups.
age_bins = [18, 25, 35, 45, 55, 65, 75, np.inf]
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
df['Age_Group']= pd.cut(df['Customer_Age'], bins= age_bins,labels=age_labels,right=False)

# Premium collected from several age groups
premium_agegroup = df.groupby('Age_Group', observed= False )['Premium_Amount'].mean().round(2)
print("\n2.b - Average Premium paid by several Age Groups:")
print(premium_agegroup)

# Premium collected from all genders
premium_gender = df.groupby('Customer_Gender',observed= False )['Premium_Amount'].mean().round(2).reset_index()
print("\n2.b - Average Premium paid by different Genders:")
print(premium_gender)

# Making pie chart showing the contribution of different age groups in the total premium collected in all the FYs
plt.figure(figsize = (12,8))
plt.subplot(1,2,1)
plt.pie(
    x=premium_agegroup,
    labels=age_labels,
    colors=sns.color_palette('pastel'),
    autopct='%1.1f%%',
    startangle=90,
    shadow=True
)
plt.title('Premium paid by Age Group')
plt.axis('equal')
plt.subplots_adjust(wspace=0.3) #This function creates space between two charts.
plt.tight_layout()

# Making a bar chart using seaborn showing the premium collection to the different genders
plt.subplot(1,2,2)
sns.barplot(
    x='Customer_Gender',
    y='Premium_Amount',
    data=premium_gender,
    palette='pastel',
    hue='Customer_Gender' ,
    legend=False
)
plt.title('Premium paid by diffrent Genders')
plt.xlabel('Gender')
plt.ylabel('Premium Amount')
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)
plt.show()


# 2.c Investigate geographical sales distribution (Customer_Location).

# Summary of the policies sold in all the states and premium collected.
top_states= df['State'].value_counts().head(10).reset_index()
top_states.columns = ['State', 'Policy_Count']
print("\n2.c - Top 10 States by Number of Policies Sold:")
print(top_states)

plt.figure(figsize = (12,6))
plt.bar(
    top_states['State'],
    top_states['Policy_Count'],
    color= "red",
    width = 0.5
)
plt.xticks(rotation=45)
plt.title('Top 10 States by Number of Policies Sold. ')
plt.xlabel('State')
plt.ylabel('Number of Policies Sold')
plt.tight_layout()
plt.show()

# 3.a Compare the performance of different Sales_Channel in terms of policies sold and premium generated.

# Primium collection summery fo different sales channals
Sales_channel= df.groupby("Sales_Channel").agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum')
).sort_values('Total_Premium',ascending=False ).reset_index()
print("\n3.a - Policies sold by all the sales channels and the premium collected:")
print(Sales_channel)

# PLotting bar graphs(Graph 1) showing the total premium collected form all the channals.
plt.figure(figsize = (15,10))
plt.subplot(1,2,1)
sns.barplot(
    x='Sales_Channel',
    y='Total_Premium',
    data=Sales_channel,
    hue='Sales_Channel',
    legend= False,
    palette='plasma'
)
plt.xticks(rotation=45)
plt.title('Total Premium collected by the Sales Channels')
plt.xlabel('Sales Channel')
plt.ylabel('Total Premium')
plt.subplots_adjust(wspace=0.5)
plt.tight_layout()

# PLotting bar graphs(Graph 1) showing the total policies sold form all the channals.
plt.subplot(1,2,2)
sns.barplot(
    x='Sales_Channel',
    y='Total_Policies',
    data=Sales_channel,
    hue='Sales_Channel',
    legend= False,
    palette='YlGnBu'
)
plt.title('Policies sold by Sales Channels')
plt.xticks(rotation=45)
plt.subplots_adjust(wspace=0.5)
plt.xlabel('Sales Channel')
plt.ylabel('Total Policies in Thousends')
plt.tight_layout()
plt.show()


# 3.b Identify which channels are most effective for specific policy types.

# We will be plotting 4 pie charts showing the sales channal selling the different policy types in each financial year.
Sales_channel2= df.groupby(["Sales_Channel", "Policy_Type"]).agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum')
).sort_values('Policy_Type',ascending=False ).reset_index()
print("\n3.b - Most popular policy in the Financial Year:")
print(Sales_channel2)
channel_policy_type_pivot = df.groupby(['Sales_Channel', 'Policy_Type']).size().unstack(fill_value=0)

channels = Sales_channel2['Sales_Channel'].unique()
plt.figure(figsize=(14,5*len(channels)))

for i, channel in enumerate(channels, start=1):
    # Filter data for that channel and draw graphs for all
    data = Sales_channel2[Sales_channel2['Sales_Channel'] == channel]

    plt.subplot(len(channels), 2, i)
    plt.pie(
        data['Total_Policies'],
        labels=data['Policy_Type'],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette('pastel')
    )
    plt.title(f'Policy Type Distribution for {channel}')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()



# 4.a Determine the claim rate (percentage of policies with claims).

# Summary of the total claims
Claim_rate = df['Has_Claimed'].value_counts(normalize=True) * 100
print(f"\nClaim Rate:\n{Claim_rate}")

plt.figure(figsize = (10,10))
sns.countplot(
    x='Has_Claimed',
    data=df,
    palette= 'husl'
)
plt.title('Claim Rate Distribution')
plt.xlabel('Claim Rate (%)')
plt.ylabel('Count of policies ')
plt.xticks(ticks=(0,1), labels=('No Claim', 'Claimed'))
plt.show()


# 4.b Analyze the average Claim_Amount by Policy_Type and Customer_Age.

# Summary of avg claimes made in all the policy type
Avg_claim= df[df['Has_Claimed']==True].groupby('Policy_Type')['Claim_Amount'].mean().sort_values(ascending=True).reset_index()
print('\n4.b - Average claims per policy type:')
print(Avg_claim)

# Summary of the avg claim in the different age groups.
Avg_claim_age = df.groupby('Age_Group', observed = False )['Has_Claimed'].mean().reset_index()
Avg_claim_age['Has_Claimed'] = (Avg_claim_age['Has_Claimed'] * 100).round(2)
Avg_claim_age.rename(columns={'Has_Claimed':'Claim_Rate'}, inplace=True)
print("\n4.b - Claim Rate by Age Group:")
print(Avg_claim_age)

# This bar chart will show all the policy type and the claim amount
plt.figure(figsize = (12,6))
sns.barplot(
    data= Avg_claim,
    x="Policy_Type",
    y="Claim_Amount",
    hue="Policy_Type",
    legend=False,
    palette="colorblind",
)
plt.xticks(rotation=45)
plt.title("Average clams per Policy Type")
plt.xlabel("Age Group")
plt.ylabel("Claim Amount")
plt.tight_layout()
plt.show()

# This bar chart will show you the claim amount of all the age groups
plt.figure(figsize = (12,6))
sns.barplot(
    data = Avg_claim_age,
    x="Age_Group",
    y="Claim_Rate",
    hue="Age_Group",
    legend=False,
    palette="magma",
)
plt.xticks(rotation=45)
plt.title("Average claims per Age Group")
plt.xlabel("Age Group")
plt.ylabel("Claim Rate(%)")
plt.tight_layout()
plt.show()


#4.c Explore if certain customer demographics are more prone to claims and the premium collected.

# Summary of claimes in all the states.
state_claim = df[df['Has_Claimed']==True].groupby('State')['Claim_Amount'].mean().sort_values(ascending=True).reset_index().round(2)
print("\nClaims amount per State:")
print(state_claim)

# This bar chart will show the claim amount and all the states
plt.figure(figsize=(12, 8))
sns.barplot(
    data=state_claim,
    x= 'State',
    y='Claim_Amount',
    hue='State',
    legend=False,
    palette='YlGnBu',
)
plt.title('Claim Amount to all the States ' )
plt.xlabel('State')
plt.xticks(rotation=60, ha='right') #used 'ha' to allign the names of all the states below there bars
plt.ylabel('Claim Amount (In Millions)')
plt.tight_layout()
plt.show()

# summary of the total premium collected from all the states
state_claim = df.groupby('State')['Premium_Amount'].mean().sort_values(ascending=True).reset_index().round(2)
print("\nPremium Amount collected per State:")
print(state_claim)

# This bar chart will show the total premium collected from all the states
plt.figure(figsize=(12, 8))
sns.barplot(
    data=state_claim,
    x= 'State',
    y='Premium_Amount',
    hue='State',
    legend=False,
    palette='husl',
)
plt.title('Claim Amount to all the States ' )
plt.xlabel('State')
plt.xticks(rotation=60, ha='right') #used 'ha' to allign the names of all the states below there bars
plt.ylabel('Premium Amount (In Millions)')
plt.tight_layout()
plt.show()

# 4.d Compare the states which poses high premium to claim ratio

# Just summary of adding the premium amount and the claim ammount.
state_ratio = df.groupby('State', observed=False).agg({
    'Premium_Amount':'sum',
    'Claim_Amount':'sum'
})

# Calculating the premium to claim ratio of all the states
state_ratio['Premium_ratio'] = (state_ratio['Premium_Amount']/state_ratio['Claim_Amount']*100).replace([float('inf'), float('nan')], 0).round(2)
print("Primium to claim ratio of all the states:- \n")
print(state_ratio)

# Top 10 states with low claim ratio thus thess can be said to be a profitable state
top_state = state_ratio.sort_values('Premium_ratio', ascending = False).head(10)
print("\nPrimium to claim ratio of top 10 states:- ")
print(top_state)

# Top 10 states with highest claim ratio which make them a risky state to do business
risky_state = state_ratio.sort_values('Premium_ratio', ascending = True).head(10)
print("\n Primium to claim ratio of top 10 high risky states:- ")
print(risky_state)

# This bar chart will show the claim ratio of all the states
plt.figure(figsize=(12, 8))
sns.barplot(
    x='State',
    y='Premium_ratio',
    hue='State',
    data=state_ratio,
    legend=False,
    palette='colorblind',
)
plt.xticks(rotation=45,ha='right')
plt.xlabel('State')
plt.ylabel('Premium  / Claim ratio')
plt.title('Premium to claim ratio vs. State')
plt.tight_layout()
plt.show()

# Chart will show the top 10 states with high claim ration means premium is collected more and the claims are less
plt.figure(figsize=(12, 8))
sns.barplot(
    x='State',
    y='Premium_ratio',
    data=top_state,
    hue='State',
    legend=False,
    palette='dark',

)
plt.xticks(rotation=45,ha='right')
plt.xlabel('State')
plt.ylabel('Premium to Claim ratio in %')
plt.title('Premium to claim ratio vs. State')
plt.tight_layout()
plt.show()

# Chart will show the top 10 states with low claim ratio which means there is more claims than premium collected

plt.figure(figsize=(12, 8))
sns.barplot(
    x='State',
    y='Premium_ratio',
    data=risky_state,
    hue='State',
    legend=False,
    palette='dark',

)
plt.xticks(rotation=45,ha='right')
plt.xlabel('State')
plt.ylabel('Premium to Claim ratio in %')
plt.title('Premium to claim ratio vs. State')
plt.tight_layout()
plt.show()

# Analysis on the basis of Quarters and Financial years
# Defining the function for financial years
def get_financial_year(date):
    if date.month >= 4:
        return f"{date.year}-{date.year + 1}"
    else:
        return f"{date.year - 1}-{date.year}"
df['Financial_Year'] = df['Sale_Date'].apply(get_financial_year)

# Defining Quarters
def get_financial_quarter(date):
    if 4 <= date.month <= 6:
        return 'Quarter I'
    elif 7 <= date.month <= 9:
        return 'Quarter II'
    elif 10 <= date.month <= 12:
        return 'Quarter III'
    else:
        return 'Quarter IV'
df['Financial_Quarter'] = df['Sale_Date'].apply(get_financial_quarter)

# Creating the premium collection summary of all Financial years and Quarters
summary = df.groupby(['Financial_Year', 'Financial_Quarter']).agg(
    Total_Policies=('Policy_ID', 'count'),
    Total_Premium=('Premium_Amount', 'sum')
).reset_index()
print('Summary of Policies with Finencial year and Quarter:- \n')
print(summary)

financial_years = summary['Financial_Year'].unique()

# Making the pie chart of all the quarters of the financial year showing the %age of policies sold in that financial year.
for i, fy in enumerate(financial_years, start = 1) :
    data = summary[summary['Financial_Year'] == fy]

    plt.figure(figsize=(12, 8))
    plt.pie(
        x = data['Total_Policies'],
        labels=data['Financial_Quarter'],
        autopct='%1.1f%%',
        startangle=90,
        shadow=False,
        explode= [0.02] * len(data),
        colors=sns.color_palette('pastel')
    )
    plt.title(f'Total Policies Distribution - FY {fy}', fontsize='12')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Making the bar chart of all the quarters of the financial year showing the count of policies sold in that financial year.
for i, Fy in enumerate(financial_years, start=1):
    data = summary[summary['Financial_Year'] == Fy]

    plt.figure(figsize=(12, 8))
    bar_plot=sns.barplot(
        x='Financial_Quarter',
        y='Total_Policies',
        hue='Financial_Quarter',
        legend=False,
        palette='pastel',
        data = data,
        errorbar= None,
    )
    for bar in bar_plot.patches: # this loop use to give the count of all the policies in all the querters and write them above the bars
        height = bar.get_height()
        bar_plot.text(
            bar.get_x() + bar.get_width() / 2,
            height + 50,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10
        )
    plt.title(f'Total Policies Distribution - FY {Fy}', fontsize='12')
    plt.ylabel('Total Premium')
    plt.xlabel('Quarter')
    plt.tight_layout()
    plt.show()

# Bar chart of the Quarters and the total premium collected
plt.figure(figsize=(12, 6))
sns.barplot(
    x='Financial_Quarter',
    y='Total_Premium',
    hue='Financial_Year',
    data=summary,
    palette='Set2',
    legend=False
)
plt.title('Quarter-wise Premium Collection across Financial Years')
plt.ylabel('Total Premium')
plt.xlabel('Quarter')
plt.tight_layout()
plt.show()

# This line will show the count of policies sold in the quarter
plt.figure(figsize=(12, 6))
sns.lineplot(
    x='Financial_Quarter',
    y='Total_Policies',
    hue='Financial_Year',
    data=summary,
    marker='o',
    linestyle='-',
)
plt.title('Quarter-wise Policy Sales Trend')
plt.ylabel('Number of Policies')
plt.xlabel('Quarter')
plt.tight_layout()
plt.show()

# Here you will get the summary of total premium in different quarters of all the financial years
pivot = summary.pivot(index='Financial_Year', columns='Financial_Quarter', values='Total_Premium')
print("\nPremium by Financial Year & Quarter:")
print(pivot)

# Here you will get the summary of total count of policies sold in different quarters of all the financial years
pivot2 = summary.pivot(index='Financial_Year', columns='Financial_Quarter', values='Total_Policies')
print("\nTotal policies by Financial Year & Quarter:")
print(pivot2)

# Monthly sales of policies and the total premium collected from them.

df['Month_Name']= df['Sale_Date'].dt.strftime('%B')
df['Month_Num']= df['Sale_Date'].dt.month

Month_sales = df.groupby(['Month_Name', 'Financial_Year','Month_Num']).agg(
    Total_Policies = ('Policy_ID','count'),
    Total_Premium = ('Premium_Amount','sum'),
    Total_Claim = ('Claim_Amount','sum')
).reset_index()
print(Month_sales)

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

