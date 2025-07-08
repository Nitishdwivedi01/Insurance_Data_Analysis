# Importing the required libraries
# We can also use sqlite3 but I have used sqlalchamy because it is bit easy

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# reading the csv file and using it to upload data in the db
csv_file_path = r"C:\Users\Nitish kumar\PyCharmMiscProject\Insurance data analysis\Insurance_sales_data.csv"
df = pd.read_csv(csv_file_path)

# MySQL connection details which the pandas will use to connect with the DB
username = "root"
password = "Mysql%4012345"
host = "localhost"
database = "insurance_data_analysis"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")

# Uploading the data from csv to MySQL table (append mode)
# df.to_sql(
#     name="insurance_policies",  # table name, before uploading the data make sure you have table
#     con=engine,
#     if_exists="append",
#     index=False
# )
print("✅ Data uploaded successfully!")
print('Ready to run Queries:- \n')

#  We have to create table, and database in sql so that we can specify it while uploading the data

# Creating table,
q1 = """
CREATE TABLE insurance_policies (
    Policy_ID VARCHAR(20),
    Customer_ID VARCHAR(20),
    Policy_Type VARCHAR(20),
    Premium_Amount BIGINT,
    Coverage_Amount FLOAT,
    Policy_Start_Date DATE,   -- Formate should be YYYY-MM-DD for all the dates
    Policy_End_Date DATE,
    Payment_Frequency VARCHAR(20),
    Policy_Status VARCHAR(20),
    Customer_Age INT,
    Customer_Gender VARCHAR(10),
    Customer_Location VARCHAR(100),
    State VARCHAR(50),
    Sales_Agent_ID VARCHAR(20),
    Sales_Channel VARCHAR(20),
    Sale_Date DATE,
    Financial_Year VARCHAR(10),
    Has_Claimed BOOLEAN,
    Claim_Amount BIGINT
);
"""
# df = pd.read_sql(q1, engine)
# print(df)

# Running this test query
q2 = """
select * from insurance_policies limit 20;
"""
df = pd.read_sql(q2, engine)
print(df)


q3 = """
-- Count of policies that has been claimed and not claimed in all the states 

SELECT 
    State,
    COUNT(*) AS Total_Policies,
    SUM(CASE WHEN Has_Claimed = TRUE THEN 1 ELSE 0 END) AS Claimed_Policies,
    SUM(CASE WHEN Has_Claimed = FALSE THEN 1 ELSE 0 END) AS Unclaimed_Policies
FROM insurance_policies
GROUP BY State
ORDER BY Total_Policies DESC;
"""
df = pd.read_sql(q3, engine)
print(df)

q4 = """
-- Analyze the total premium amount and number of policies sold each financial year
SELECT 
    Financial_Year,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Financial_Year;
"""
df = pd.read_sql(q4, engine)
print(df)


q5 = """
-- Identify the most popular policy types and their contribution to total premiums
SELECT 
    Policy_Type, SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Policy_Type;
 

"""
df = pd.read_sql(q5, engine)
print(df)


q6 = """
-- Examine sales trends across different policy types over the three financial years
SELECT 
    Financial_Year, Policy_Type, COUNT(Policy_ID)
FROM
    insurance_policies
GROUP BY Financial_Year , Policy_Type
ORDER BY Financial_Year , Policy_Type;
"""
df = pd.read_sql(q6, engine)
print(df)

q7 = """
-- Understand the age distribution of policyholders and how age influence policy purchases and premium amounts.
SELECT 
  CASE 
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
		WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
    ELSE 'Unknown'
  END AS Age_Group,
  COUNT(*) AS Total_Customers, sum(Premium_Amount) as Total_Premium
FROM insurance_policies
GROUP BY Age_Group
ORDER BY Age_Group;  
"""
df = pd.read_sql(q7, engine)
print(df)

q8 = """
 -- Explore how gender influence on policy purchases and premium amounts.
 SELECT 
    Customer_Gender,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Customer_Gender
ORDER BY Customer_Gender;
"""

df = pd.read_sql(q8, engine)
print(df)


q9 = """
-- Investigate geographical sales distribution (Customer_Location).
SELECT 
    State,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY State
ORDER BY Total_Policy DESC;
"""

df = pd.read_sql(q9, engine)
print(df)

q10 = """
-- Compare the performance of different Sales_Channel in terms of policies sold and premium generated.
SELECT 
    Sales_channel,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Sales_Channel
ORDER BY Total_Premium;
    
-- Also finding the data with respect the different financial year.
SELECT 
    Financial_Year,
    Sales_channel,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Sales_Channel , Financial_Year
ORDER BY Total_Premium;
"""
df = pd.read_sql(q10, engine)
print(df)


q11 = """
-- Identify which channels are most effective for specific policy types.
select Sales_Channel, Policy_Type from ( select Policy_Type, Sales_Channel, count(*) as Policy_count, 
ROW_NUMBER() over (Partition by Sales_Channel order by count(*) desc) as New  from insurance_policies group by Policy_Type, Sales_Channel) 
as Ranked where New = 1;
  
"""
df = pd.read_sql(q11, engine)
print(df)

q12 = """
-- Determine the claim rate basis of Gender, Sales channel, Financial year, Policy type, State (percentage of policies with claims)
-- Avg Claim rate
SELECT 
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies;
 
 -- Avg Claim rate basis of Gender
 SELECT 
 Customer_Gender,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Customer_Gender order by Customer_Gender desc;
 
  -- Avg Claim rate basis of Sales channel
  SELECT 
 Sales_Channel,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Sales_Channel order by Sales_Channel desc;
 
 -- Avg Claim rate basis of Policy Type
SELECT 
 Policy_Type,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Policy_Type order by Policy_Type desc;
    
 -- Avg Claim rate basis of Financial year
 SELECT 
 Financial_Year,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Financial_Year order by Financial_Year desc;
    
 -- Avg Claim rate basis of States
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg desc;
"""
df = pd.read_sql(q12, engine)
print(df)

q13 = """
-- Analyze the average Claim_Amount by Policy_Type and Customer_Age
-- Part 1
-- This will give the count of policies claimed in each Policy Type 
SELECT 
    Policy_Type,
    SUM(CASE
        WHEN Has_Claimed = TRUE THEN 1
        ELSE 0
    END) AS 'Count of Policy claimed'
FROM
    insurance_policies
GROUP BY Policy_Type
ORDER BY Policy_Type DESC;

-- This will give the count of policies not claimed in each Policy Type 
SELECT 
    Policy_Type,
    SUM(CASE
        WHEN Has_Claimed = FALSE THEN 1
        ELSE 1
    END) AS 'Count of Policy claimed'
FROM
    insurance_policies
GROUP BY Policy_Type
ORDER BY Policy_Type DESC;

-- Part 2
-- This give the total amount of policies claime in all the age groups also we will check for the policy count along with Premium
SELECT 
    CASE
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
		WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
        ELSE 'Unknown'
    END AS Age_Group,
    ROUND(AVG(Claim_Amount), 2) AS 'Avg Claim Amount',
    COUNT(Policy_ID) AS 'Total policy claimed'
FROM
    insurance_policies
WHERE
    Has_Claimed = TRUE
GROUP BY Age_Group
ORDER BY Age_Group;
"""
df = pd.read_sql(q13, engine)
print(df)

q14 = """
-- This give the total amount of policies not claimed in all the age groups also we will check for the policy count along with Premium 
SELECT 
    CASE
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
		WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
        ELSE 'Unknown'
    END AS Age_Group,
    ROUND(AVG(Claim_Amount), 2) AS 'Avg Claim Amount',
    COUNT(Policy_ID) AS 'Total policy claimed'
FROM
    insurance_policies
WHERE
    Has_Claimed = false
GROUP BY Age_Group
ORDER BY Age_Group;
"""
df = pd.read_sql(q14, engine)
print(df)

q15 = """
-- Explore if certain customer demographics are more prone to claims and the premium collected.
SELECT 
    State,
    SUM(CASE
        WHEN Has_Claimed = TRUE THEN 1
        ELSE 0
    END) AS 'Count of Policies Claimed',
    SUM(CASE
        WHEN Has_Claimed = FALSE THEN 1
        ELSE 0
    END) AS 'Count of Policies Not Claimed',
    ROUND(SUM(DISTINCT CASE
                WHEN Has_Claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS 'Claim rate',
    SUM(Premium_Amount) AS 'Total premium collected'
FROM
    insurance_policies
GROUP BY State
ORDER BY 'Claim rate' DESC;
    
-- Top 10 states with high claim ratio thus these can be said to be a risky state
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg desc limit 10;

-- Top 10 states with low claim ratio thus these can be said to be a profitable state
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg limit 10;
"""
df = pd.read_sql(q15, engine)
print(df)


try:
    # Your database logic
    ...
    print("SQL executed successfully.")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()